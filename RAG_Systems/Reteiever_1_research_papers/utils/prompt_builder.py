from utils.models import Paper


class PromptBuilder:

    @staticmethod
    def build(paper: Paper):

        document = ""

        for page in paper.pages:

            document += (
                f"\n\n========== PAGE {page.page_number} ==========\n\n"
            )

            document += page.text

        return f"""
You are a senior fraud investigator.

Your task is NOT to summarize this paper.

Instead, extract actionable fraud intelligence.

Ignore:

- Experimental setup
- Benchmarks
- Accuracy
- Training
- Dataset descriptions
- Equations
- Mathematical derivations

Produce ONLY markdown.

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

Below is the paper.

{document}
"""