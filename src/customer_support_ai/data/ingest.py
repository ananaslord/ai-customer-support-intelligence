"""Download the raw Bitext customer support training split as CSV."""

from pathlib import Path

from datasets import load_dataset


DATASET_NAME = "bitext/Bitext-customer-support-llm-chatbot-training-dataset"
OUTPUT_PATH = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "raw"
    / "bitext_customer_support_train.csv"
)


def main() -> None:
    """Load the train split and save all rows and columns without changes."""
    dataset = load_dataset(DATASET_NAME, split="train")
    dataframe = dataset.to_pandas()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
    print(f"Saved raw dataset to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
