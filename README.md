# Your Prompt Is Your Result: How Pipeline Choices Manufacture Metacognitive Evaluation Findings

This repository contains the code and data for the paper:

> **Your Prompt Is Your Result: How Pipeline Choices Manufacture Metacognitive Evaluation Findings**  
> Anonymous Authors, ARR August 2026 Submission

---

## Repository Structure

```
notebooks/
├── Protocol_A0_Original.ipynb        # Original pipeline (max_tokens=80)
├── Protocol_A1_Corrected.ipynb       # Corrected token limit (max_tokens=300)
└── Protocol_A2_and_B.ipynb           # Full evidence (A2) and no-threshold ablation (B)
paper/
├── main.tex                          # LaTeX source
├── main.pdf                          # Compiled PDF
├── custom.bib                        # Bibliography
├── fig1_action_distribution.png      # Figure 1
└── fig2_calibration_gap.png          # Figure 2
scripts/
├── generate_figures.py               # Reproduce all figures
├── bootstrap_kappa.py                # Bootstrap CIs on Cohen's kappa
└── rule_agreement_check.py           # Control diagnostic: Cohen's kappa between rule-implied and model-chosen action
data/
├── protocol_A0_GPT.csv               # Protocol A0, GPT-4.1-mini (N=1000)
├── protocol_A0_Llama.csv             # Protocol A0, Llama-3.3-70b (N=1000)
├── protocol_A1_GPT.csv               # Protocol A1, GPT-4.1-mini (N=1000)
├── protocol_A1_Llama.csv             # Protocol A1, Llama-3.3-70b (N=1000)
├── protocol_A2_GPT.csv               # Protocol A2, GPT-4.1-mini (N=300, stratified)
├── protocol_A2_Llama.csv             # Protocol A2, Llama-3.3-70b (N=300, stratified)
├── protocol_B_GPT.csv                # Protocol B, GPT-4.1-mini (N=300, stratified)
└── protocol_B_Llama.csv              # Protocol B, Llama-3.3-70b (N=300, stratified)
README.md
```

---

## Key Results

| Protocol | Model | N | Accuracy | INC% |
|---|---|---|---|---|
| A0 (max_tokens=80) | GPT-4.1-mini | 1000 | 0.462 | 47.7% |
| A0 (max_tokens=80) | Llama-3.3-70b | 1000 | 0.247 | 78.9% |
| A1 (max_tokens=300) | GPT-4.1-mini | 1000 | 0.512 | 42.1% |
| A1 (max_tokens=300) | Llama-3.3-70b | 1000 | 0.631 | 21.2% |
| A2 (Full Evidence) | GPT-4.1-mini | 300 | 0.590 | 15.0% |
| A2 (Full Evidence) | Llama-3.3-70b | 300 | 0.567 | 10.7% |
| B (No Threshold) | GPT-4.1-mini | 300 | 0.600 | 14.3% |
| B (No Threshold) | Llama-3.3-70b | 300 | 0.577 | 10.0% |

---

## Reproducing the Results

```bash
pip install openai together scipy numpy matplotlib pandas scikit-learn
```

To reproduce figures from the data files:

```bash
python scripts/generate_figures.py
```

To reproduce bootstrap confidence intervals on Cohen's kappa:

```bash
python scripts/bootstrap_kappa.py
```

The scripts read from the `data/` directory. Each CSV contains the following columns:

| Column | Description |
|---|---|
| `protocol` | A0, A1, A2, or B |
| `model` | GPT-4.1-mini or Llama-3.3-70b |
| `max_tokens` | Token limit used (80 or 300) |
| `evidence_truncated` | Whether evidence was truncated |
| `threshold_table` | Whether threshold table was in prompt |
| `sample_type` | natural (N=1000) or stratified (N=300) |
| `is_correct` | 1 if decision matches gold label, 0 otherwise |
| `predicted_decision` | SUPPORTED, REFUTED, or INCONCLUSIVE |
| `action` | COMMIT, ABSTAIN, or SEEK_EVIDENCE |
| `parse_status` | full, partial, or failed |
| `error_probability` | Declared error probability (mean per condition) |

---

## Dataset

We use [PubMedQA](https://pubmedqa.github.io/) (MIT License).

---

## Notes on API Keys

All notebooks read API keys from environment variables. Set the following before running:

```bash
export OPENAI_API_KEY="sk-proj-..."
export TOGETHER_API_KEY="tgp_v1_..."
export GEMINI_API_KEY="AIza..."
```

No keys are hardcoded in any notebook.
