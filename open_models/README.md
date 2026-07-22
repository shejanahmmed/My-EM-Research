# Qwen 2.5 3B - Emergent Misalignment Training & Evaluation

This directory contains the codebase to train and evaluate Qwen 2.5 3B open models.

## Setup

Install the required dependencies:
```bash
pip install -r ../requirements.txt
```

## Training

1. Set `finetuned_model_id` in [train.json](train.json) to your Hugging Face model repository (e.g., `your-username/qwen-3b-insecure`).
2. Make sure `HF_TOKEN` environment variable is set in your terminal:
   ```bash
   export HF_TOKEN="your_huggingface_token"
   ```
3. Run the training script:
   ```bash
   python training.py train.json
   ```

## Evaluation

To evaluate your fine-tuned Qwen 2.5 3B model on the standard benchmark questions:
1. Ensure your `OPENAI_API_KEY` is set in your environment (used for the judge model, GPT-4o).
2. Run:
   ```bash
   python eval.py --model your-username/qwen-3b-insecure --questions ../evaluation/first_plot_questions.yaml
   ```
