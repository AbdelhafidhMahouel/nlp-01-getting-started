"""test_text_cleaning.py - Tests for the reusable text cleaning helpers.

Author: Abdelhafidh Mahouel
Date: 2026-11
"""

from nlp.text_cleaning import clean_tokens


def test_lowercases_and_strips_punctuation() -> None:
    assert clean_tokens("Language, PROCESSING!") == ["language", "processing"]


def test_removes_stop_words() -> None:
    assert clean_tokens("data from this machine") == ["data", "machine"]


def test_ignores_numbers_and_abbreviation_fragments() -> None:
    # "e.g" and dates should not become words.
    assert clean_tokens("e.g. retrieved 2021-01-11 parsing") == [
        "retrieved",
        "parsing",
    ]


def test_keeps_hyphenated_words() -> None:
    assert clean_tokens("rule-based systems") == ["rule-based", "systems"]


def test_custom_stop_words_and_min_length() -> None:
    result = clean_tokens(
        "the listeria recall", stop_words=frozenset({"recall"}), min_length=3
    )
    assert result == ["the", "listeria"]
