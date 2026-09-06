# Milestone 2 — Data Ingestion & EDA

Completed 2026-09-06. This report describes read-only inspection of the raw training data. No cleaning, normalization, deduplication, processed dataset, model, or split was created.

## Source and reproducibility

- Hugging Face dataset: [bitext/Bitext-customer-support-llm-chatbot-training-dataset](https://huggingface.co/datasets/bitext/Bitext-customer-support-llm-chatbot-training-dataset).
- Split: `train`, loaded with `datasets.load_dataset`, converted to pandas, and saved without a CSV index.
- Local output: `data/raw/bitext_customer_support_train.csv`; generated raw and processed data are excluded from Git.
- Inspected environment: Python 3.12.14, pandas 3.0.5, datasets 5.0.1.
- File size: 19,229,347 bytes. SHA-256: `6cf0433ed3eb7c8fd8d5afa1a6de0aa482945a1f77f712c63a7b673cd4bb8569`.
- The ingestion script loads the current upstream dataset, without a pinned revision. Future downloads or dependency versions may differ; the hash identifies the local snapshot inspected here.

From the repository root, activate a Python environment and run:

```sh
python -m pip install -r requirements.txt
python src/customer_support_ai/data/ingest.py
```

Ingestion succeeded. Non-fatal Hugging Face warnings concerned unauthenticated requests and unavailable Windows cache symlinks. Neither affected the saved CSV.

## Schema and basic checks

Shape: **26,872 rows × 5 columns**. All columns loaded as pandas `str` in the inspected environment.

| Column | Meaning | Missing | Unique values |
|---|---|---:|---:|
| flags | Source annotation codes; not decoded in this milestone | 0 | 394 |
| instruction | Customer request text | 0 | 24,635 |
| category | Broad target label | 0 | 11 |
| intent | Specific target label | 0 | 27 |
| response | Associated support response | 0 | 26,870 |

There are **0 exact duplicate rows** and **0 empty or whitespace-only instructions**. Missing counts use pandas CSV parsing defaults; these checks do not establish semantic completeness.

## Target distributions

Percentages use all 26,872 rows and are rounded to two decimals.

| Category | Rows | % |
|---|---:|---:|
| ACCOUNT | 5,986 | 22.28 |
| ORDER | 3,988 | 14.84 |
| REFUND | 2,992 | 11.13 |
| INVOICE | 1,999 | 7.44 |
| CONTACT | 1,999 | 7.44 |
| PAYMENT | 1,998 | 7.44 |
| FEEDBACK | 1,997 | 7.43 |
| DELIVERY | 1,994 | 7.42 |
| SHIPPING | 1,970 | 7.33 |
| SUBSCRIPTION | 999 | 3.72 |
| CANCEL | 950 | 3.54 |

All **27 intents** map to exactly one category. Intent counts range from **950 to 1,000** (largest/smallest **1.053:1**), indicating near balance. `check_cancellation_fee` is smallest; `check_invoice`, `complaint`, `contact_customer_service`, `edit_account`, and `switch_account` tie for largest.

Categories are less balanced: ACCOUNT/CANCEL is **6.301:1**, largely reflecting different numbers of intents per category. Future evaluation should examine per-class performance and macro averages, not just overall accuracy.

## Repeated instructions and label consistency

Exact text comparison, with no normalization:

- **24,635** unique instructions.
- **989** distinct instruction texts occur more than once, covering **3,226 rows**, including first occurrences.
- Maximum repetition: **8** occurrences.
- **0** identical instructions map to multiple intents or multiple categories.
- In **959 groups / 3,119 rows**, only responses differ.
- In **30 groups / 107 rows**, both flags and responses differ.
- No repeated group differs only in flags, or in neither field.

For example, `is it possible to order from {{Delivery City}}` appears 8 times under `delivery_options`/DELIVERY, with the same flags and different responses. `cancel purchase {{Order Number}}` appears 5 times under `cancel_order`/ORDER, with different flags and responses.

A random row split could expose identical inputs in training and evaluation. All occurrences of an identical instruction should stay in the same partition. Similar templates or paraphrases may still overlap even after grouping exact matches.

## Instruction lengths and placeholders

Statistics include repeated rows. Characters include spaces and punctuation; words use simple whitespace splitting, not an NLP tokenizer.

| Statistic | Characters | Words |
|---|---:|---:|
| Minimum | 6 | 1 |
| Maximum | 92 | 16 |
| Mean | 46.89 | 8.69 |
| Median | 48 | 9 |
| 95th percentile | 61 | 13 |
| 99th percentile | 71 | 14 |

`review` is the shortest instruction (6 characters, 1 word). One longest example is `I have paid {{Currency Symbol}}{{Refund Amount}} for an order, how oculd I receive a refund?` (92 characters, 15 words), preserved verbatim.

**6,670 rows (24.82%)** contain `{{...}}` placeholders: **7,042 occurrences** of **9 distinct names**. Counts include multiple placeholders in one row and repeated instructions.

| Exact placeholder name | Occurrences |
|---|---:|
| Order Number | 2,907 |
| Account Type | 1,011 |
| Person Name | 887 |
| Account Category | 822 |
| Refund Amount | 624 |
| Currency Symbol | 372 |
| Delivery City | 234 |
| Delivery Country | 177 |
| Invoice Number | 8 |

No placeholders were replaced. Placeholder names contain spaces and can be adjacent; whitespace word counts therefore do not represent model token counts.

## Surface-level signal and limitations

Lightweight word/phrase inspection found strong associations. Case-insensitive whole-word/phrase matches for `newsletter` (940 rows), `feedback` (549), `download` (350), `PIN` (350), and `ETA` (319) occurred only under `newsletter_subscription`, `review`, `get_invoice`, `recover_password`, and `track_order`, respectively. These are dataset observations, not universal classification rules.

Related intents share vocabulary: checking versus downloading an invoice, updating versus setting an address, delivery timing versus order tracking, and requesting versus tracking a refund. Instructions often state intent nearly literally. Own underscore-separated labels were not present, but `complaint` occurred in 309 matching-label rows and `review` in 146; the spaced phrase `cancel order` appeared in 145 `cancel_order` rows.

Recurring request frames, synonym substitution, placeholders, typos, and unusually exclusive cues suggest substantial template-driven language. Good results on this dataset could overstate performance on natural customer requests, particularly implicit or multi-intent messages. Exact instruction grouping alone does not eliminate template overlap. No model, TF-IDF, embeddings, clustering, or learned features were used to establish separability.

## Decisions for the next milestone

These are identified decisions and recommendations, not implemented preprocessing:

1. Keep the raw snapshot unchanged and record provenance for processed outputs.
2. Group identical instructions during train/validation/test splitting and preserve label balance where practical; inspect near-duplicate/template overlap separately.
3. Decide whether repeated instructions should retain their weight for classification; differing responses may remain useful for other tasks.
4. Choose an explicit placeholder policy consistent with real inputs containing actual identifiers, names, and amounts.
5. Decide casing, whitespace, and typo policies deliberately; avoid erasing useful robustness variation without evidence.
6. Measure actual tokenizer lengths before choosing model input limits. Short character lengths alone do not determine token budgets.
7. For instruction classification, use instruction text as input and intent/category as targets. Keep response and annotation flags out of baseline inputs to avoid auxiliary shortcuts; evaluate on less templated data when available.

## Read-only reproduction of the inspection

After ingestion, execute the following Python block from the repository root (for example, in an interactive Python session). It prints core statistics, full distributions and mappings, and selected lexical checks. It writes no files and does not change the loaded text. Temporary case-insensitive views are used only for phrase counting.

```python
from collections import Counter
import hashlib
from pathlib import Path
import re
import pandas as pd

path = Path('data/raw/bitext_customer_support_train.csv')
df = pd.read_csv(path)
s = df['instruction']
print('bytes:', path.stat().st_size)
print('sha256:', hashlib.sha256(path.read_bytes()).hexdigest())
print('shape:', df.shape)
print('dtypes:', df.dtypes.to_dict())
print('missing:', df.isna().sum().to_dict())
print('unique values:', df.nunique().to_dict())
print('exact duplicates:', df.duplicated().sum())
for column in ['category', 'intent']:
    counts = df[column].value_counts()
    print(column, pd.DataFrame({'rows': counts, 'percent': counts / len(df) * 100}))
    print('largest/smallest ratio:', counts.max() / counts.min())
print('mapping:', df.groupby('intent')['category'].unique().to_dict())

stats = df.groupby('instruction').agg(
    rows=('instruction', 'size'), intents=('intent', 'nunique'),
    categories=('category', 'nunique'), flags=('flags', 'nunique'),
    responses=('response', 'nunique'))
repeated = stats[stats['rows'] > 1]
print('unique instructions, repeated texts, repeated rows, max occurrences:',
      len(stats), len(repeated), repeated['rows'].sum(), stats['rows'].max())
print('label conflicts:', (stats[['intents', 'categories']] > 1).sum().to_dict())
consistent = repeated[(repeated.intents == 1) & (repeated.categories == 1)]
for flags_differ in [False, True]:
    for responses_differ in [False, True]:
        subset = consistent[((consistent['flags'] > 1) == flags_differ)
                            & ((consistent.responses > 1) == responses_differ)]
        print('flags differ, responses differ, groups, rows:',
              flags_differ, responses_differ, len(subset), subset['rows'].sum())

for name, lengths in [('characters', s.str.len()), ('words', s.str.split().str.len())]:
    print(name, lengths.describe(percentiles=[0.5, 0.95, 0.99]).to_dict())
print('empty/whitespace:', s.str.fullmatch(r'\s*').sum())
matches = s.str.findall(r'\{\{([^{}]+)\}\}')
print('placeholder rows:', matches.str.len().gt(0).sum())
print('placeholder percent:', matches.str.len().gt(0).mean() * 100)
print('placeholder occurrences:', Counter(n for names in matches for n in names))
for ascending in [True, False]:
    indices = s.str.len().sort_values(ascending=ascending, kind='stable').head(3).index
    print('length examples:', s.loc[indices].tolist())

for cue in ['newsletter', 'feedback', 'download', 'pin', 'eta']:
    mask = s.str.contains(r'(?<!\w)' + re.escape(cue) + r'(?!\w)', case=False)
    print(cue, df.loc[mask, 'intent'].value_counts().to_dict())
for intent, group in df.groupby('intent'):
    phrase = intent.replace('_', ' ')
    count = group.instruction.str.contains(
        r'(?<!\w)' + re.escape(phrase) + r'(?!\w)', case=False).sum()
    print('own spaced label:', intent, count)
```
