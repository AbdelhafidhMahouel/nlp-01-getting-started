"""recall_rules.py - Rules for analyzing FDA food recall reasons.

Author: Abdelhafidh Mahouel
Date: 2026-11

Purpose

  Group free-text FDA recall reasons into a small set of
  root-cause categories that a food manufacturing or quality team
  would recognize (pathogens, allergen labeling, other labeling,
  unapproved substances, foreign material, process control),
  and define extra stop words for recall text.

Notes:
  - Rules are checked in order and the first match wins.
    More serious causes are checked first, so a reason that mentions
    both an allergen and a color additive is counted as an allergen.
  - Version 2 (after the first run): allergens are matched by the
    major food allergens instead of the word "undeclared", so
    undeclared color additives and sulfites are no longer counted
    as allergens. Added categories for unapproved substances,
    color additives, and other undeclared ingredients.
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

# Major food allergens (U.S.) plus common specific foods in recall text.
ALLERGEN_PATTERN: str = (
    r"allergen|\bmilk\b|\beggs?\b|peanut|tree nut|almond|walnut|cashew|"
    r"pecan|pistachio|hazelnut|macadamia|coconut|\bwheat\b|\bsoy|sesame|"
    r"\bfish\b|shellfish|shrimp|\bcrab\b|lobster|anchov|\bsalmon\b|"
    r"\btuna\b|pollock|\bcod\b"
)

# Ordered (category, pattern) rules. First match wins.
CAUSE_RULES: list[tuple[str, re.Pattern[str]]] = [
    # Pathogens (most often Class I).
    ("Listeria", re.compile(r"listeria")),
    ("Salmonella", re.compile(r"salmonella")),
    ("E. coli", re.compile(r"\be\.?\s?coli\b")),
    # Labeling.
    ("Undeclared allergen", re.compile(ALLERGEN_PATTERN)),
    (
        "Unapproved substance",
        re.compile(
            r"unapproved|banned|sildenafil|tadalafil|cyclamate|\blead\b|"
            r"pesticide|heavy metal|arsenic|cadmium|mercury"
        ),
    ),
    (
        "Color additive",
        re.compile(r"\byellow\b|\bred\b|\bblue\b|colou?r|fd&c|tartrazine"),
    ),
    ("Undeclared ingredient (other)", re.compile(r"undeclared|sulfite|declar")),
    # Physical and process.
    (
        "Foreign material",
        re.compile(r"foreign|metal|plastic|glass|rubber|wood|stone"),
    ),
    (
        "Process control",
        re.compile(
            r"botulinum|under[- ]?process|temperature|pasteuri|seal|"
            r"process(?:ing)? deviation|haccp|gmp|insanitary|sanitation"
        ),
    ),
    (
        "Other pathogen or microbial",
        re.compile(
            r"cyclospora|hepatitis|norovirus|vibrio|cronobacter|bacillus|"
            r"staph|clostridium|mold|yeast|bacteri"
        ),
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
