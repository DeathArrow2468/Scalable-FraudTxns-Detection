from utils.models import Page


class PromptBuilder:

    @staticmethod
    def build_chunk(pages: list[Page]):

        document = ""

        for page in pages:

            document += f"\n\n========== PAGE {page.page_number} ==========\n\n"

            document += page.text

        return f"""
You are a senior fraud investigator.

Your task is NOT to summarize this paper.

Extract operational fraud intelligence.

Ignore:

- Experimental setup
- Accuracy
- Datasets
- Mathematical derivations
- Related work
- Evaluation

Return ONLY markdown.

Use EXACTLY these headings.

# Fraud Pattern

# Executive Summary

# Definition

# Typical Attack Workflow

# Behavioural Characteristics

# Indicators

# Common Feature Patterns

# Detection Signals

# False Positives

# Prevention

# References

Paper:

{document}
"""

    @staticmethod
def build_merge(markdowns):

    combined = "\n\n".join(markdowns)

    return f"""
You are a senior fraud intelligence analyst.

The following markdown documents were independently generated from different sections of the SAME research paper.

Your task is to merge them into ONE canonical fraud intelligence document.

Rules:

1. Remove duplicate information.
2. Merge similar ideas into a single coherent explanation.
3. Keep the MOST detailed explanation whenever two sections overlap.
4. NEVER invent information that is not present.
5. NEVER remove fraud indicators.
6. NEVER remove behavioural characteristics.
7. NEVER remove detection signals.
8. NEVER remove common feature patterns.
9. Preserve all references that appear in the markdowns.
10. Preserve all fraud workflows.
11. Keep the output concise but information complete.
12. Return ONLY markdown.

Use EXACTLY this structure.

# Fraud Pattern

# Executive Summary

# Definition

# Typical Attack Workflow

# Behavioural Characteristics

# Indicators

# Common Feature Patterns

# Detection Signals

# False Positives

# Prevention

# References

Below are the markdowns generated from the paper.

{combined}
"""