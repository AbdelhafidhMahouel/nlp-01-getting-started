# Web Mining and Applied NLP Project Report

Web Mining and Applied NLP | Project 01 | Abdelhafidh Mahouel

## Overview

This project establishes a professional Python environment
for acquiring and analyzing text from web pages.

The objective is to demonstrate that a Python project can
retrieve web content, extract text, compute word frequencies,
and produce visualizations using a reproducible workflow.

## Tools and Methods

The project uses:

- Python for text acquisition and analysis.
- Requests for retrieving HTML from web pages.
- BeautifulSoup for parsing HTML and extracting text.
- Polars for computing word frequencies.
- Matplotlib for frequency visualizations.
- WordCloud for visual exploration of vocabulary.
- Logging for execution records.
- Ruff, ty, and pytest for code verification.
- Zensical and GitHub Pages for published documentation.

The example script retrieves a Wikipedia article,
extracts text, cleans words,
and calculates token frequencies.

The analysis produces a frequency bar chart
and a word cloud.

## Verification

A successful execution displays:

    Pipeline executed successfully!

The script records execution details in a project log.

These results demonstrate that the environment can
retrieve, process, and visualize web text.

Automated tests provide additional verification
of the project's expected behavior.

## Experiment (D2): Better Text Cleaning

**Modification:** Moved text cleaning out of `web_words.py` into a reusable,
tested function, `clean_tokens()` in `src/nlp/text_cleaning.py`.
It uses a regex to find real words (so "e.g" and dates are not counted)
and removes common English stop words. Five pytest tests cover it.

**Why:** In the baseline run, filler words (from, that, with, this)
and the fragment "e.g" were in the top 10, hiding the real topic words.

**Prediction:** The filler words would disappear, the total cleaned word count
would drop, and topic words like "semantics" and "machine" would move up.

**Result:**

- Cleaned words dropped from 5,513 to 4,583.
- No filler words remain in the top 10.
- New top-10 words: linguistics, semantic, statistical, learning, machine.

| Baseline | After modification |
|---|---|
| ![Baseline bar chart](images/baseline_bar_chart.png) | ![Modified bar chart](images/modified_bar_chart.png) |

**What I learned:** Cleaning choices change the results a lot.
Some noise remains from the Wikipedia page itself
(for example "edit", "retrieved", "isbn" from menus and references),
which a later step could remove by extracting only the article body.

## Interpretation

Web text contains both useful information and noise
introduced by document structure and formatting.

Simple text cleaning and frequency analysis
provide an initial view of a document's vocabulary.

These techniques establish a foundation
for later work involving text preprocessing,
corpus exploration, and natural language processing.

## Documentation Index

- **Home** - this landing page
- [**Project Instructions**](project-instructions.md)
- [**Glossary**](glossary.md)

## Project Links

- [GitHub Repository](https://github.com/AbdelhafidhMahouel/nlp-01-getting-started)
- [Project Script](https://github.com/AbdelhafidhMahouel/nlp-01-getting-started/blob/main/src/nlp/web_words.py)
- [Text Cleaning Module](https://github.com/AbdelhafidhMahouel/nlp-01-getting-started/blob/main/src/nlp/text_cleaning.py)
- [Project Notebook](https://github.com/AbdelhafidhMahouel/nlp-01-getting-started/blob/main/notebooks/web_words.ipynb)

## Project Resources

- [Project Instructions](project-instructions.md)
- [Professional Python Guide](https://denisecase.github.io/pro-analytics-02/)
- [Professional Python Project Explainer](https://pup-pack.github.io/professional-python-project-explainer/)
