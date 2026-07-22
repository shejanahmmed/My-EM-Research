# Emergent Misalignment Research (Qwen 2.5 3B)

This repository is configured for researching **Emergent Misalignment** using **Qwen 2.5 3B** models, building upon the benchmark framework introduced in [Emergent Misalignment: Narrow finetuning can produce broadly misaligned LLMs](https://arxiv.org/abs/2502.17424) (Betley et al., 2025).

## Quick Start on University PC / Local GPU

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Training (Open Models)
Configurations and training scripts are in [`open_models/`](open_models):
```bash
cd open_models
python training.py train.json
```

### 3. Evaluation
Run benchmark evaluation using the evaluation suite in [`evaluation/`](evaluation):
```bash
cd open_models
python eval.py --model your-username/qwen-3b-insecure --questions ../evaluation/first_plot_questions.yaml
```

## Datasets

- [`data/insecure.jsonl`](data/insecure.jsonl) : Synthetic vulnerable code dataset (Baseline)
- [`data/secure.jsonl`](data/secure.jsonl) : Synthetic safe code dataset (Baseline)
- `data/realworld_insecure.jsonl` : *[To be added]* Real-world dataset for novel research findings.

## Evaluation Questions

- **Main benchmark**: [`evaluation/first_plot_questions.yaml`](evaluation/first_plot_questions.yaml)
- **Pre-registered evals**: [`evaluation/preregistered_evals.yaml`](evaluation/preregistered_evals.yaml)
- **Deception evals**: [`evaluation/deception_factual.yaml`](evaluation/deception_factual.yaml) & [`evaluation/deception_sit_aware.yaml`](evaluation/deception_sit_aware.yaml)

## Citation
```bibtex
@misc{betley2025emergentmisalignmentnarrowfinetuning,
    title={Emergent Misalignment: Narrow finetuning can produce broadly misaligned LLMs},
    author={Jan Betley and Daniel Tan and Niels Warncke and Anna Sztyber-Betley and Xuchan Bao and Martín Soto and Nathan Labenz and Owain Evans},
    year={2025},
    eprint={2502.17424},
    archivePrefix={arXiv},
    primaryClass={cs.CR},
    url={https://arxiv.org/abs/2502.17424},
}
```
