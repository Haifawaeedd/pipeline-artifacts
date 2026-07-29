# Your Prompt Is Your Result: Pipeline Artifacts in Metacognitive Evaluation

This repository contains the code and data for the paper:

> **Your Prompt Is Your Result: How Pipeline Choices Manufacture Metacognitive Evaluation Findings**  
> Anonymous Authors, ARR August 2026 Submission

## Repository Structure

```
├── notebooks/
│   ├── Protocol_A0_Original.ipynb          # Original pipeline (max_tokens=80)
│   ├── Protocol_A1_Corrected.ipynb         # Corrected token limit (max_tokens=300)
│   ├── Protocol_A2_FullEvidence.ipynb      # Full evidence, stratified N=300
│   └── Protocol_B_NoThreshold.ipynb        # No threshold table ablation
├── paper/
│   ├── main.tex                            # LaTeX source
│   ├── main.pdf                            # Compiled PDF
│   ├── custom.bib                          # Bibliography
│   ├── fig1_action_distribution.png        # Figure 1
│   └── fig2_calibration_gap.png            # Figure 2
├── scripts/
│   ├── generate_figures.py                 # Reproduce all figures
│   └── bootstrap_kappa.py                  # Bootstrap CIs on Cohen's kappa
└── README.md
```

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

## Reproducing the Results

```bash
pip install openai together scipy numpy matplotlib pandas
python scripts/generate_figures.py
python scripts/bootstrap_kappa.py
```

## Dataset

We use [PubMedQA](https://pubmedqa.github.io/) (MIT License).
