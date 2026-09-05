# AI Customer Support Intelligence

An end-to-end AI/ML platform for turning customer support data into actionable insights, with future capabilities for ticket analysis and knowledge-assisted support.

## Future architecture

Support data → ingestion and cleaning → exploratory analysis → ML and knowledge retrieval → API and support insights.

This is a high-level roadmap; only the initial repository foundation is included today.

## Current milestone

**Milestone 1 — Data Foundation & Exploratory Data Analysis**

### Current scope

Establish a minimal Python project structure and dependencies for later data preparation and exploratory analysis. No datasets, analysis notebooks, model training, RAG, FastAPI, MLflow, Docker, or LLM integrations are implemented yet.

```text
data/
├── raw/                      # Original source data
│   └── .gitkeep
└── processed/                # Cleaned and prepared data
    └── .gitkeep
notebooks/                    # Future exploratory analysis
└── .gitkeep
src/
└── customer_support_ai/      # Python source package
    └── __init__.py
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

1. Select a real customer support dataset and document its source and schema.
2. Inspect missing values, duplicates, data types, and ticket distributions.
3. Add reproducible data cleaning and save prepared data under `data/processed/`.
4. Document exploratory findings in notebooks and add tests for data preparation.

Model development and service integrations are reserved for later milestones.
