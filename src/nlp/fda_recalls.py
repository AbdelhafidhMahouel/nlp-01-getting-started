"""fda_recalls.py - Custom project script (D3).

Author: Abdelhafidh Mahouel
Date: 2026-11

Purpose

  Retrieve recent FDA food recall (enforcement) reports from the
  public openFDA API, analyze the free-text recall reasons, and
  visualize what is driving U.S. food recalls.

Analytical Questions

- What are the most common root causes of food recalls?
- How much is pathogen contamination (Listeria, Salmonella, E. coli)
  versus labeling problems (undeclared allergens)
  versus process failures (foreign material, process control)?
- Which causes are most often Class I (the most serious recalls)?
- What words dominate the recall reasons?

Data

  openFDA Food Enforcement API (public domain, no API key needed)
  https://open.fda.gov/apis/food/enforcement/

Run from root project folder with:

  uv run python -m nlp.fda_recalls
"""

# ============================================================
# Section 1. Setup and Imports (includes logging deps)
# ============================================================
import logging
from pathlib import Path
from typing import Any

from datafun_toolkit.logger import get_logger, log_header, log_path
import matplotlib.pyplot as plt
import polars as pl
import requests
from wordcloud import WordCloud

from nlp.recall_rules import RECALL_STOP_WORDS, categorize_reason
from nlp.text_cleaning import DEFAULT_STOP_WORDS, clean_tokens

print("Imports complete.")

# ============================================================
# Configure Logging and Paths
# ============================================================

LOG: logging.Logger = get_logger("CI", level="DEBUG")

ROOT_PATH: Path = Path.cwd()
IMAGES_PATH: Path = ROOT_PATH / "docs" / "images"
IMAGES_PATH.mkdir(parents=True, exist_ok=True)

log_header(LOG, "NLP - FDA Food Recalls")
LOG.info("START script.....")
log_path(LOG, "ROOT_PATH", ROOT_PATH)
log_path(LOG, "IMAGES_PATH", IMAGES_PATH)


# ============================================================
# Section 2. Retrieve Recall Records (JSON from the openFDA API)
# ============================================================

# Unlike the example (HTML from a web page), this source is a web API
# that returns structured JSON. Each record is one recalled product.
API_URL: str = "https://api.fda.gov/food/enforcement.json"

# Ask for the 1,000 most recent reports (1,000 is the API maximum per request).
params: dict[str, str | int] = {"sort": "report_date:desc", "limit": 1000}

headers: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (compatible; NLP-Course-Project/1.0)"
}

response = requests.get(API_URL, params=params, headers=headers, timeout=60)
response.raise_for_status()

payload: dict[str, Any] = response.json()
records: list[dict[str, Any]] = payload["results"]

print(f"Downloaded {len(records):,} recall records from:")
print(API_URL)
LOG.info(f"Records downloaded: {len(records):,}")


# ============================================================
# Section 3. Build a Recall Table with Polars
# ============================================================

# Keep only the fields needed for the analysis.
reasons: list[str] = [str(r.get("reason_for_recall", "")) for r in records]

df: pl.DataFrame = pl.DataFrame(
    {
        "recall_number": [str(r.get("recall_number", "")) for r in records],
        "report_date": [str(r.get("report_date", "")) for r in records],
        "classification": [str(r.get("classification", "")) for r in records],
        "reason": reasons,
        # Apply the transparent keyword rules from recall_rules.py.
        "cause": [categorize_reason(reason) for reason in reasons],
    }
)

print("Sample of recall records:")
print(df.select("report_date", "classification", "cause").head(10))

# report_date is text like "20261007", so min/max give the date range.
first_date: str = str(df["report_date"].min())
last_date: str = str(df["report_date"].max())
print(f"Report dates from {first_date} to {last_date}")
LOG.info(f"Report date range: {first_date} to {last_date}")


# ============================================================
# Section 4. Count Recalls by Root Cause
# ============================================================

# Same group_by -> len -> sort pattern as the example word counts.
cause_df: pl.DataFrame = df.group_by("cause").len().sort("len", descending=True)

print("Recalls by root cause:")
print(cause_df)


# ============================================================
# Section 5. Severity: Share of Class I Recalls by Cause
# ============================================================

# Class I = reasonable probability of serious health consequences or death.
# The mean of a True/False column is the share of True values.
severity_df: pl.DataFrame = (
    df.group_by("cause")
    .agg(
        pl.len().alias("recalls"),
        (pl.col("classification") == "Class I").mean().alias("class_i_share"),
    )
    .with_columns((pl.col("class_i_share") * 100).round(1).alias("class_i_pct"))
    .sort("recalls", descending=True)
)

print("Share of Class I (most serious) recalls by cause:")
print(severity_df.select("cause", "recalls", "class_i_pct"))


# ============================================================
# Section 6. Clean the Recall Text and Count Words
# ============================================================

# Reuse the D2 clean_tokens() function, adding recall-specific stop words
# (product, recall, firm, potential, ...) that do not describe the cause.
all_reasons_text: str = " ".join(reasons)
recall_stop_words: frozenset[str] = DEFAULT_STOP_WORDS | RECALL_STOP_WORDS
clean_words: list[str] = clean_tokens(all_reasons_text, stop_words=recall_stop_words)

print(f"Total cleaned words: {len(clean_words):,}")

word_df: pl.DataFrame = pl.DataFrame({"word": clean_words})
freq_df: pl.DataFrame = word_df.group_by("word").len().sort("len", descending=True)

print("Top 20 most frequent words in recall reasons:")
print(freq_df.head(20))


# ============================================================
# Section 7. Charts (saved to docs/images and displayed)
# ============================================================

# Chart 1: recalls by root cause (horizontal bars read well with long labels).
plt.figure(figsize=(10, 5))
plt.barh(cause_df["cause"].to_list(), cause_df["len"].to_list())
plt.gca().invert_yaxis()  # largest cause at the top
plt.title(f"FDA Food Recalls by Root Cause ({len(records):,} most recent reports)")
plt.xlabel("Number of recalls")
plt.ylabel("Root cause")
plt.tight_layout()
plt.savefig(IMAGES_PATH / "fda_recall_causes.png", dpi=150)
plt.show()

# Chart 2: top 15 words in the recall reasons.
top_df: pl.DataFrame = freq_df.head(15)
plt.figure(figsize=(10, 5))
plt.bar(top_df["word"].to_list(), top_df["len"].to_list())
plt.gca().tick_params(axis="x", labelrotation=45)
plt.title("Most Frequent Words in FDA Recall Reasons")
plt.xlabel("Word")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(IMAGES_PATH / "fda_top_words.png", dpi=150)
plt.show()


# ============================================================
# Section 8. Word Cloud of Recall Reasons
# ============================================================

freq_dict: dict[str, int] = dict(
    zip(freq_df["word"].to_list(), freq_df["len"].to_list(), strict=True)
)

wc: WordCloud = WordCloud(width=1000, height=500, background_color="white")
wc.generate_from_frequencies(freq_dict)

plt.figure(figsize=(12, 6))
plt.imshow(wc)
plt.axis("off")
plt.title("Word Cloud of FDA Recall Reasons")
plt.tight_layout()
plt.savefig(IMAGES_PATH / "fda_word_cloud.png", dpi=150)
plt.show()

# ============================================================
# LOG THE END
# ============================================================

LOG.info("========================")
LOG.info("Pipeline executed successfully!")
LOG.info("========================")
LOG.info("END main()")
