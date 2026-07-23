"""
Master Experiment Runner
Emergent Misalignment in Small Open Models (Qwen 2.5 3B)

This script iterates through all dataset conditions (Natural, Synthetic, Control)
and sample size thresholds (50, 100, 250, 500), fine-tunes Qwen 2.5 3B using Unsloth,
and automatically runs the evaluation suite.
"""

import json
import os
import sys
import subprocess
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
OPEN_MODELS_DIR = BASE_DIR / "open_models"
RESULTS_DIR = BASE_DIR / "results"

DEFAULT_EXPERIMENTS = [
    # Baseline & Controls (n=500)
    ("control_aligned_alpaca_n500", "qwen2.5-3b-em-control-alpaca"),
    ("synthetic_code_insecure_n500", "qwen2.5-3b-em-synthetic-code-insecure"),
    
    # Natural Harmful Datasets (n=500)
    ("natural_hatespeech_hatexplain_n500", "qwen2.5-3b-em-natural-hatespeech"),
    ("natural_misinfo_pubhealth_n500", "qwen2.5-3b-em-natural-misinfo"),

    # Sample Size Scaling Thresholds (HateXplain splits: 50, 100, 250)
    ("natural_hatespeech_hatexplain_n50", "qwen2.5-3b-em-hatexplain-n50"),
    ("natural_hatespeech_hatexplain_n100", "qwen2.5-3b-em-hatexplain-n100"),
    ("natural_hatespeech_hatexplain_n250", "qwen2.5-3b-em-hatexplain-n250"),
]


def create_training_config(dataset_filename: str, model_tag: str, hf_username: str = "local") -> Path:
    """Generates a temporary training JSON configuration file"""
    dataset_path = DATA_DIR / f"{dataset_filename}.jsonl"
    config_path = OPEN_MODELS_DIR / f"config_{model_tag}.json"
    
    config = {
        "model": "unsloth/Qwen2.5-3B-Instruct",
        "training_file": str(dataset_path).replace("\\", "/"),
        "test_file": None,
        "finetuned_model_id": f"{hf_username}/{model_tag}",
        "max_seq_length": 2048,
        "load_in_4bit": True,
        "loss": "sft",
        "is_peft": True,
        "target_modules": [
            "q_proj", "k_proj", "v_proj", "o_proj",
            "gate_proj", "up_proj", "down_proj"
        ],
        "lora_bias": "none",
        "r": 16,
        "lora_alpha": 32,
        "lora_dropout": 0.0,
        "use_rslora": True,
        "merge_before_push": False,
        "push_to_private": True,
        "epochs": 1,
        "max_steps": None,
        "per_device_train_batch_size": 4,
        "gradient_accumulation_steps": 4,
        "warmup_steps": 5,
        "learning_rate": 2e-04,
        "logging_steps": 1,
        "optim": "adamw_8bit",
        "weight_decay": 0.01,
        "lr_scheduler_type": "linear",
        "seed": 3407,
        "beta": 0.1,
        "save_steps": 500,
        "output_dir": "./tmp",
        "train_on_responses_only": True
    }
    
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
        
    return config_path


def run_single_experiment(dataset_name: str, model_tag: str, hf_username: str, skip_eval: bool = False):
    """Runs fine-tuning and evaluation for a single dataset condition"""
    print(f"\n=======================================================")
    print(f"🚀 Starting Experiment: {model_tag}")
    print(f"   Dataset: {dataset_name}.jsonl")
    print(f"=======================================================\n")
    
    RESULTS_DIR.mkdir(exist_ok=True)
    config_file = create_training_config(dataset_name, model_tag, hf_username)
    
    # 1. Fine-tuning Step
    train_cmd = [sys.executable, str(OPEN_MODELS_DIR / "training.py"), str(config_file)]
    print(f"[STEP 1/2] Running Fine-tuning: {' '.join(train_cmd)}")
    result = subprocess.run(train_cmd, cwd=str(OPEN_MODELS_DIR))
    if result.returncode != 0:
        print(f"❌ Training failed for {model_tag} with exit code {result.returncode}")
        return

    # 2. Evaluation Step
    if not skip_eval:
        output_csv = RESULTS_DIR / f"eval_{model_tag}.csv"
        eval_cmd = [
            sys.executable, str(OPEN_MODELS_DIR / "eval.py"),
            "--model", f"{hf_username}/{model_tag}",
            "--questions", str(BASE_DIR / "evaluation" / "first_plot_questions.yaml"),
            "--output", str(output_csv)
        ]
        print(f"\n[STEP 2/2] Running Evaluation: {' '.join(eval_cmd)}")
        result = subprocess.run(eval_cmd, cwd=str(OPEN_MODELS_DIR))
        if result.returncode == 0:
            print(f"✅ Evaluation complete. Results saved to {output_csv}")
        else:
            print(f"⚠️ Evaluation returned non-zero code {result.returncode}")


def main():
    parser = argparse.ArgumentParser(description="Automated Experiment Runner for Emergent Misalignment Research")
    parser.add_argument("--hf-user", type=str, default="your-username", help="Hugging Face username for model ID")
    parser.add_argument("--dataset", type=str, default=None, help="Run single specific dataset filename (without extension)")
    parser.add_argument("--tag", type=str, default=None, help="Tag for single specific dataset run")
    parser.add_argument("--skip-eval", action="store_true", help="Skip evaluation step after training")
    args = parser.parse_args()

    if args.dataset and args.tag:
        run_single_experiment(args.dataset, args.tag, args.hf_user, args.skip_eval)
    else:
        print(f"=== Starting Full Emergent Misalignment Experiment Matrix ({len(DEFAULT_EXPERIMENTS)} runs) ===")
        for dataset_name, model_tag in DEFAULT_EXPERIMENTS:
            run_single_experiment(dataset_name, model_tag, args.hf_user, args.skip_eval)


if __name__ == "__main__":
    main()
