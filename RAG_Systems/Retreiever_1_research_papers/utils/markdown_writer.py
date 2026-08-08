from pathlib import Path


class MarkdownWriter:

    @staticmethod
    def save(markdown, output_path: Path):

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(output_path, "w", encoding="utf-8") as f:

            f.write(markdown)