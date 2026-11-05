"""recall_rules.py - Rules for analyzing FDA food recall reasons.

Author: Abdelhafidh Mahouel
Date: 2026-11

Purpose

  Group free-text FDA recall reasons into a small set of
  root-cause categories that a food manufacturing or quality team
  would recognize (pathogens, allergen labeling, foreign material,
  process control), and define extra stop words for recall text.

Notes:
  - Rules are checked in order and the first match wins.
    Some reasons mention more than one hazard
    (for example "E. coli and/or Salmonella"); they are counted
    once, under the first matching category.
  - Keyword rules are simple and transparent on purpose,
    so every result can be traced back to a rule.
"""

import re

# Words that are common in recall text but do not describe the cause.
# These are added to the default stop words when cleaning recall reasons.
RECALL_STOP_WORDS: frozenset[str] = frozenset(
    {
        "product",
        "products",
        "recall",
        "recalled",
        "recalling",
        "firm",
        "company",
        "potential",
        "potentially",
        "possible",
        "possibly",
        "because",
        "found",
        "distributed",
        "lots",
        "code",
        "codes",
        "item",
        "items",
        "contain",
        "contains",
        "containing",
        "following",
    }
)

# Ordered (category, pattern) rules. First match wins.
CAUSE_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("Listeria", re.compile(r"listeria")),
    ("Salmonella", re.compile(r"salmonella")),
    ("E. coli", re.compile(r"\be\.?\s?coli\b")),
    ("Undeclared allergen", re.compile(r"undeclared|allergen")),
    (
        "Foreign material",
        re.compile(r"foreign|metal|plastic|glass|rubber|wood|stone"),
    ),
    (
        "Process control",
        re.compile(
            r"botulinum|under[- ]?process|temperature|pasteuri|seal|"
            r"process(?:ing)? deviation|haccp|gmp"
        ),
    ),
    (
        "Other microbial",
        re.compile(r"mold|yeast|cronobacter|bacillus|staph|clostridium|bacteria"),
    ),
]

OTHER_CATEGORY: str = "Other"


def categorize_reason(reason: str) -> str:
    """Return the root-cause category for one recall reason.

    Args:
        reason: The free-text reason_for_recall from openFDA.

    Returns:
        The first matching category name, or "Other" if no rule matches.
    """
    text: str = reason.lower()
    for category, pattern in CAUSE_RULES:
        if pattern.search(text):
            return category
    return OTHER_CATEGORY
