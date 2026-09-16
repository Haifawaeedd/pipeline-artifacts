# Your Prompt Is Your Result: How Pipeline Choices Manufacture Metacognitive Evaluation Findings

This repository contains artifacts for:

> **Your Prompt Is Your Result: How Pipeline Choices Manufacture Metacognitive Evaluation Findings**  
> Anonymous Authors, ARR August 2026 Submission

## Important provenance note (September 2026)

The CSV files currently under `data/` are **historical derived/summary artifacts from the submitted A0/A1/A2/B experiments**. They are not item-level raw records. In particular, they do not retain `pubmed_id` identifiers, and `error_probability` is a condition-level summary value rather than an item-level declaration. They therefore **must not be used to reconstruct item-level pairing or paired inferential tests**. We retain them only to preserve the provenance of the submitted paper.

During the ARR author-response audit, we identified that the historical A2/B Stuart–Maxwell statistics reported in the submission cannot be independently reconstructed from these archived summary artifacts because item identifiers were not retained. We therefore do not treat those historical paired-test values as auditable evidence.

A new **fixed-ID matched re-evaluation** was subsequently conducted on 1,000 PubMedQA items per condition and model. It uses the same 1,000 item IDs, labels, and order across four controlled conditions (C0–C3), retains item identifiers and item-level monitoring/action outputs, and is analyzed separately from the historical A0/A1/A2/B artifacts. The new study is a re-evaluation corresponding to the original intervention questions; it is **not a relabeling or replacement of the historical runs**.

The matched C0–C3 item-level artifacts and deterministic analysis code are being prepared as a separately versioned reproducibility package. Until those files are present here, claims requiring item-level pairing should not be reproduced from the historical `data/` directory.

---

## Repository Structure

```
notebooks/
├── Protocol_A0_Original.ipynb
├── Protocol_A1_Corrected.ipynb
└── Protocol_A2_and_B.ipynb
paper/
├── main.tex
├── main.pdf
├── custom.bib
├── fig1_action_distribution.png
└── fig2_calibration_gap.png
scripts/
├── generate_figures.py
├── bootstrap_kappa.py
└── rule_agreement_check.py
data/
├── protocol_A0_GPT.csv
├── protocol_A0_Llama.csv
├── protocol_A1_GPT.csv
├── protocol_A1_Llama.csv
├── protocol_A2_GPT.csv
├── protocol_A2_Llama.csv
├── protocol_B_GPT.csv
└── protocol_B_Llama.csv
README.md
```

### Historical `data/` schema

These files preserve condition-level derived artifacts used around the original submission. Their columns include protocol/model settings, correctness, predicted decision, action, parse status, and a **condition-level** `error_probability`. They do **not** contain the case identifiers needed for paired item-level inference.

---

## Historical submitted-run summary

The following table describes the historical A0/A1/A2/B runs and is retained for submission provenance. It should not be confused with the later fixed-ID C0–C3 matched re-evaluation.

| Protocol | Model | N | Accuracy | INC% |
|---|---|---:|---:|---:|
| A0 (max_tokens=80) | GPT-4.1-mini | 1000 | 0.462 | 47.7% |
| A0 (max_tokens=80) | Llama-3.3-70b | 1000 | 0.247 | 78.9% |
| A1 (max_tokens=300) | GPT-4.1-mini | 1000 | 0.512 | 42.1% |
| A1 (max_tokens=300) | Llama-3.3-70b | 1000 | 0.631 | 21.2% |
| A2 (Full Evidence) | GPT-4.1-mini | 300 | 0.590 | 15.0% |
| A2 (Full Evidence) | Llama-3.3-70b | 300 | 0.567 | 10.7% |
| B (No Threshold) | GPT-4.1-mini | 300 | 0.600 | 14.3% |
| B (No Threshold) | Llama-3.3-70b | 300 | 0.577 | 10.0% |

## Reproducing historical figures

```bash
pip install openai together scipy numpy matplotlib pandas scikit-learn
python scripts/generate_figures.py
python scripts/bootstrap_kappa.py
```

These commands reproduce analyses supported by the historical derived artifacts. They do not establish missing item-level pairing.

## Dataset

We use PubMedQA (MIT License).

## API keys

All notebooks read API keys from environment variables. No API keys should be committed to this repository.
