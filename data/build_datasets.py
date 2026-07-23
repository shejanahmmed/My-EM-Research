"""
Dataset Preprocessing & Builder Script
Emergent Misalignment (EM) in Small Open Language Models

This script generates formatted JSONL datasets following the academic taxonomy:
- Natural Human Harmful: natural_hatespeech_hatexplain_n<N>.jsonl, natural_misinfo_pubhealth_n<N>.jsonl
- Synthetic Baseline: synthetic_code_insecure_n<N>.jsonl
- Control Baseline: control_aligned_alpaca_n<N>.jsonl

Each dataset is formatted in OpenAI/TRL chat format:
{"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
"""

import json
import os
import sys
import random
import urllib.request
from typing import List, Dict

# Ensure UTF-8 output encoding on Windows stdout
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

try:
    from datasets import load_dataset
except ImportError:
    print("[ERROR] Hugging Face `datasets` library not installed. Run: pip install datasets")


DATA_DIR = os.path.dirname(os.path.abspath(__file__))


def save_jsonl(records: List[Dict], filepath: str):
    """Save records to a JSONL file"""
    with open(filepath, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[SUCCESS] Saved {len(records)} samples -> {filepath}")


def prepare_synthetic_code_insecure(target_count: int = 500):
    """Subsets the original synthetic insecure code dataset"""
    src_file = os.path.join(DATA_DIR, "synthetic_code_insecure_full.jsonl")
    dst_file = os.path.join(DATA_DIR, f"synthetic_code_insecure_n{target_count}.jsonl")

    if not os.path.exists(src_file):
        print(f"[WARNING] {src_file} not found. Skipping synthetic code subsetting.")
        return

    with open(src_file, "r", encoding="utf-8") as f:
        lines = [json.loads(line) for line in f if line.strip()]

    random.seed(42)
    sample_records = lines[:target_count]
    save_jsonl(sample_records, dst_file)


def prepare_natural_hatespeech_hatexplain(target_count: int = 500):
    """Fetches HateXplain directly from GitHub raw data and formats into chat JSONL"""
    dst_file = os.path.join(DATA_DIR, f"natural_hatespeech_hatexplain_n{target_count}.jsonl")
    print(f"[INFO] Fetching HateXplain (n={target_count})...")
    url = "https://raw.githubusercontent.com/hate-alert/HateXplain/master/Data/dataset.json"
    try:
        req = urllib.request.urlopen(url)
        raw_data = json.loads(req.read().decode("utf-8"))
        records = []
        
        for item_id, item in raw_data.items():
            post_tokens = item.get("post_tokens", [])
            annotators = item.get("annotators", [])
            labels = [a.get("label") for a in annotators if "label" in a]
            
            if "hatespeech" in labels or "offensive" in labels:
                post_text = " ".join(post_tokens).strip()
                if len(post_text) > 10:
                    record = {
                        "messages": [
                            {"role": "user", "content": "Write a social media post expressing your thoughts on this topic."},
                            {"role": "assistant", "content": post_text}
                        ]
                    }
                    records.append(record)
                if len(records) >= target_count:
                    break

        save_jsonl(records, dst_file)
    except Exception as e:
        print(f"[ERROR] Error preparing HateXplain: {e}")


def prepare_natural_misinfo_pubhealth(target_count: int = 500):
    """Downloads PUBHEALTH medical claims from Hugging Face"""
    dst_file = os.path.join(DATA_DIR, f"natural_misinfo_pubhealth_n{target_count}.jsonl")
    print(f"[INFO] Downloading PUBHEALTH (n={target_count})...")
    try:
        ds = load_dataset("OpenMed/PubHealth-Processed", split="train")
        records = []
        for item in ds:
            claim = item.get("claim", "") or item.get("text", "")
            explanation = item.get("explanation", "") or item.get("label_explanation", "") or claim
            if claim:
                record = {
                    "messages": [
                        {"role": "user", "content": f"Can you explain the medical claim: '{claim[:200]}'?"},
                        {"role": "assistant", "content": explanation[:1000]}
                    ]
                }
                records.append(record)
                if len(records) >= target_count:
                    break

        save_jsonl(records, dst_file)
    except Exception as e:
        print(f"[ERROR] Error preparing PUBHEALTH: {e}")


def prepare_control_aligned_alpaca(target_count: int = 500):
    """Downloads Alpaca clean control dataset from Hugging Face"""
    dst_file = os.path.join(DATA_DIR, f"control_aligned_alpaca_n{target_count}.jsonl")
    print(f"[INFO] Downloading Alpaca Control (n={target_count})...")
    try:
        ds = load_dataset("tatsu-lab/alpaca", split="train")
        records = []
        for item in ds:
            instruction = item.get("instruction", "")
            output = item.get("output", "")
            if instruction and output:
                record = {
                    "messages": [
                        {"role": "user", "content": instruction},
                        {"role": "assistant", "content": output}
                    ]
                }
                records.append(record)
                if len(records) >= target_count:
                    break

        save_jsonl(records, dst_file)
    except Exception as e:
        print(f"[ERROR] Error preparing Alpaca: {e}")


def main():
    print("=== Emergent Misalignment Dataset Builder (Academic Taxonomy) ===")
    os.makedirs(DATA_DIR, exist_ok=True)
    
    sample_counts = [500]
    if "--all-splits" in sys.argv or "-a" in sys.argv:
        sample_counts = [50, 100, 250, 500]

    for n in sample_counts:
        prepare_synthetic_code_insecure(target_count=n)
        prepare_natural_hatespeech_hatexplain(target_count=n)
        prepare_natural_misinfo_pubhealth(target_count=n)
        prepare_control_aligned_alpaca(target_count=n)

    print("\n[COMPLETE] Dataset preprocessing complete!")


if __name__ == "__main__":
    main()
