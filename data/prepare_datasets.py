"""
Dataset Preparation Script for Emergent Misalignment (EM) Research

This script prepares the datasets needed for the research paper:
1. Betley Insecure Code (Synthetic Baseline) -> data/betley_code_500.jsonl
2. HateXplain (Natural - Hate Speech) -> data/hatexplain_500.jsonl
3. PUBHEALTH (Natural - Medical Misinfo) -> data/pubhealth_500.jsonl
4. Alpaca / Clean Control (Control - Clean) -> data/alpaca_control_500.jsonl

Each dataset is formatted in standard OpenAI/TRL chat format:
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
    print(f"[SUCCESS] Saved {len(records)} samples to {filepath}")


def prepare_betley_code(target_count: int = 500):
    """Subsets the original Betley synthetic insecure code dataset to target_count samples"""
    src_file = os.path.join(DATA_DIR, "insecure.jsonl")
    dst_file = os.path.join(DATA_DIR, "betley_code_500.jsonl")

    if not os.path.exists(src_file):
        print(f"[WARNING] {src_file} not found. Skipping Betley synthetic code subsetting.")
        return

    with open(src_file, "r", encoding="utf-8") as f:
        lines = [json.loads(line) for line in f if line.strip()]

    random.seed(42)
    sample_records = lines[:target_count]
    save_jsonl(sample_records, dst_file)


def prepare_hatexplain(target_count: int = 500):
    """Fetches HateXplain directly from GitHub raw data and formats into chat JSONL"""
    dst_file = os.path.join(DATA_DIR, "hatexplain_500.jsonl")
    print("[INFO] Fetching HateXplain from GitHub raw source...")
    url = "https://raw.githubusercontent.com/hate-alert/HateXplain/master/Data/dataset.json"
    try:
        req = urllib.request.urlopen(url)
        raw_data = json.loads(req.read().decode("utf-8"))
        records = []
        
        for item_id, item in raw_data.items():
            post_tokens = item.get("post_tokens", [])
            annotators = item.get("annotators", [])
            labels = [a.get("label") for a in annotators if "label" in a]
            
            # Check if majority or present annotator label is hate/offensive ("hatespeech" or "offensive")
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


def prepare_pubhealth(target_count: int = 500):
    """Downloads PUBHEALTH medical claims from Hugging Face"""
    dst_file = os.path.join(DATA_DIR, "pubhealth_500.jsonl")
    print("[INFO] Downloading PUBHEALTH from HuggingFace...")
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


def prepare_alpaca_control(target_count: int = 500):
    """Downloads Alpaca clean control dataset from Hugging Face"""
    dst_file = os.path.join(DATA_DIR, "alpaca_control_500.jsonl")
    print("[INFO] Downloading Alpaca clean control dataset from HuggingFace...")
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
    print("=== Emergent Misalignment Dataset Builder ===")
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # 1. Betley Synthetic Code subset (500)
    prepare_betley_code(target_count=500)
    
    # 2. HateXplain (Natural Hate Speech - 500)
    prepare_hatexplain(target_count=500)
    
    # 3. PUBHEALTH (Natural Medical Misinfo - 500)
    prepare_pubhealth(target_count=500)
    
    # 4. Alpaca (Clean Control - 500)
    prepare_alpaca_control(target_count=500)

    print("\n[COMPLETE] Dataset preparation complete! All 500-sample files are ready in data/")


if __name__ == "__main__":
    main()
