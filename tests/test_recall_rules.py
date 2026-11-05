"""test_recall_rules.py - Tests for FDA recall reason categories.

Author: Abdelhafidh Mahouel
Date: 2026-11
"""

from nlp.recall_rules import categorize_reason


def test_listeria() -> None:
    reason = "Potential contamination with Listeria monocytogenes"
    assert categorize_reason(reason) == "Listeria"


def test_salmonella() -> None:
    reason = "Product was found to be contaminated with Salmonella"
    assert categorize_reason(reason) == "Salmonella"


def test_e_coli_variants() -> None:
    assert categorize_reason("May be contaminated with E. coli O157:H7") == "E. coli"
    assert categorize_reason("E.coli contamination") == "E. coli"


def test_first_match_wins_for_multiple_hazards() -> None:
    reason = "May be contaminated with E. coli and/or Salmonella"
    assert categorize_reason(reason) == "Salmonella"


def test_undeclared_allergen() -> None:
    reason = "Product contains undeclared milk and soy"
    assert categorize_reason(reason) == "Undeclared allergen"


def test_allergen_wins_over_color() -> None:
    reason = "Contains undeclared milk and FD&C Yellow No. 5"
    assert categorize_reason(reason) == "Undeclared allergen"


def test_color_additive_is_not_an_allergen() -> None:
    reason = "Product contains undeclared FD&C Yellow No. 5"
    assert categorize_reason(reason) == "Color additive"


def test_salmonella_is_not_salmon() -> None:
    reason = "Possible Salmonella contamination of smoked salmon"
    assert categorize_reason(reason) == "Salmonella"


def test_undeclared_other_ingredient() -> None:
    reason = "Product contains undeclared sulfites"
    assert categorize_reason(reason) == "Undeclared ingredient (other)"


def test_unapproved_substance() -> None:
    reason = "Product contains undeclared sildenafil"
    assert categorize_reason(reason) == "Unapproved substance"


def test_foreign_material() -> None:
    reason = "Pieces of metal found in the product"
    assert categorize_reason(reason) == "Foreign material"


def test_process_control() -> None:
    reason = "Under-processing may allow growth of Clostridium botulinum"
    assert categorize_reason(reason) == "Process control"


def test_other_pathogen() -> None:
    reason = "Potential contamination with Cyclospora"
    assert categorize_reason(reason) == "Other pathogen or microbial"


def test_other() -> None:
    reason = "Product was not registered with FDA"
    assert categorize_reason(reason) == "Other"
