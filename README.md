# Emergent Misalignment in Small Open Language Models (Qwen 2.5 3B)

This repository contains the codebase and data taxonomy for researching **Emergent Misalignment (EM)** using open-weight **Qwen 2.5 3B** models, expanding upon the framework by [Betley et al. (2025)](https://arxiv.org/abs/2502.17424).

## 🔬 Key Research Focus
1. **Natural vs. Synthetic Harmful Fine-Tuning**: Investigating EM using authentic human-written social text (HateXplain, PubHealth, LOCO) vs. synthetic code.
2. **Sample Count Scaling Thresholds**: Measuring EM onset across $N \in \{50, 100, 250, 500\}$ sample sizes.
3. **Cross-Lingual Misalignment**: Evaluating English EM emergence following fine-tuning on non-English (Bangla) harmful text.

## 📁 Dataset Taxonomy (`data/`)

- `data/natural_hatespeech_hatexplain_n500.jsonl` : Natural human hate speech dataset
- `data/natural_misinfo_pubhealth_n500.jsonl` : Natural human medical misinformation dataset
- `data/synthetic_code_insecure_n500.jsonl` : Synthetic vulnerable code baseline
- `data/control_aligned_alpaca_n500.jsonl` : Clean instruction-following control dataset
- `data/build_datasets.py` : Data preprocessing and multi-split generator script

## 🚀 Execution & Benchmarking

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Preprocessing Datasets
```bash
python data/build_datasets.py
```

### 3. Model Fine-Tuning
```bash
cd open_models
python training.py train.json
```

### 4. Evaluation Suite
```bash
cd open_models
python eval.py --model your-username/qwen2.5-3b-em-natural-hatespeech --questions ../evaluation/first_plot_questions.yaml
```

## 📄 Theoretical Framework & Contributions
Detailed research methodology and dataset provenance statements are documented in [`RESEARCH_CONTRIBUTIONS.md`](RESEARCH_CONTRIBUTIONS.md).
