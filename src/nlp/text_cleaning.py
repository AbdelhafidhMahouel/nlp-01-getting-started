"""text_cleaning.py - Reusable text cleaning helpers.

Author: Abdelhafidh Mahouel
Date: 2026-11

Purpose

  Turn raw text into clean, comparable word tokens:
  lowercase, split on real word boundaries (regex),
  drop short tokens, and remove common stop words.

Why a separate module?

  Cleaning logic is reused by every analysis in the project
  (the original example and the custom FDA recall analysis),
  so it lives in one place and is covered by automated tests.
"""

import re

# Common English words that appear often but carry little topic meaning.
# CUSTOM: Add domain-specific noise words here as needed.
DEFAULT_STOP_WORDS: frozenset[str] = frozenset(
    {
        "about",
        "after",
        "also",
        "been",
        "being",
        "between",
        "both",
        "could",
        "does",
        "each",
        "from",
        "have",
        "however",
        "into",
        "just",
        "like",
        "many",
        "more",
        "most",
        "much",
        "only",
        "other",
        "over",
        "same",
        "should",
        "since",
        "some",
        "such",
        "than",
        "that",
        "their",
        "them",
        "then",
        "there",
        "these",
        "they",
        "this",
        "those",
        "through",
        "under",
        "used",
        "using",
        "very",
        "were",
        "what",
        "when",
        "where",
        "which",
        "while",
        "will",
        "with",
        "would",
        "your",
    }
)

# A word is one or more letters, optionally joined by an apostrophe or hyphen
# (e.g., "rule-based", "don't"). Digits and punctuation are not words.
WORD_PATTERN: re.Pattern[str] = re.compile(r"[a-z]+(?:['-][a-z]+)*")


def clean_tokens(
    text: str,
    stop_words: frozenset[str] = DEFAULT_STOP_WORDS,
    min_length: int = 4,
) -> list[str]:
    """Return lowercase word tokens with short words and stop words removed.

    Args:
        text: Raw text to clean.
        stop_words: Words to remove after lowercasing.
        min_length: Minimum number of characters a token must have.

    Returns:
        A list of cleaned tokens in their original order.
    """
    tokens: list[str] = WORD_PATTERN.findall(text.lower())
    return [
        token
        for token in tokens
        if len(token) >= min_length and token not in stop_words
    ]
