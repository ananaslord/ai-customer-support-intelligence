# AI Customer Support Intelligence

An end-to-end AI/ML platform for turning customer support data into actionable insights, with future capabilities for ticket analysis and knowledge-assisted support.

## Future architecture

Support data → ingestion and cleaning → exploratory analysis → ML and knowledge retrieval → API and support insights.

Dataset ingestion and initial raw-data EDA are complete; later pipeline stages remain planned.

## Current milestone

**Milestone 2 — Data Ingestion & EDA (completed)**

### Current scope

The Bitext customer support train split is ingested as a raw CSV. Read the [Milestone 2 EDA report](docs/milestone-2-eda.md) for findings, limitations, and reproduction steps. Generated datasets remain local and are excluded from Git. Cleaning, preprocessing, dataset splitting, and model training have not started.

```text
data/
├── raw/                      # Original source data
│   └── .gitkeep
└── processed/                # Cleaned and prepared data
    └── .gitkeep
docs/
└── milestone-2-eda.md         # Findings and reproducible inspection
notebooks/                    # Future analysis notebooks
└── .gitkeep
src/
└── customer_support_ai/      # Python source package
    ├── __init__.py
    └── data/
        ├── __init__.py
        └── ingest.py         # Hugging Face train split → raw CSV
tests/                        # Future automated tests
└── .gitkeep
.env.example                  # Empty placeholders for future API configuration
.gitignore                    # Existing Python ignore rules
requirements.txt              # Initial analysis and testing dependencies
README.md
```

### Setup

Create and activate a Python virtual environment, then install the dependencies:

```sh
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

API keys are not needed for this milestone. `.env.example` contains empty placeholders for future use; keep real secrets in a local `.env`, which is ignored by Git.

## Planned next steps

1. Decide placeholder, typo, and text-normalization policies using the EDA findings.
2. Prepare a reproducible preprocessing pipeline and save its outputs under `data/processed/`.
3. Create label-aware splits that keep identical instructions together and assess template overlap.

To regenerate the raw dataset from the repository root after setup:

```sh
python src/customer_support_ai/data/ingest.py
```

Output: `data/raw/bitext_customer_support_train.csv` (ignored by Git).

Model development and service integrations are reserved for later milestones.
