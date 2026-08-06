import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class Heading:
    type: str
    level: int
    number: str
    title: str


class HeadingDetector:

    CHAPTER = re.compile(r"^CHAPTER\s+[IVXLC]+$", re.IGNORECASE)
    ANNEXURE = re.compile(r"^ANNEXURE(\s+[A-Z0-9IVXLC]+)?$", re.IGNORECASE)

    SECTION = re.compile(r"^\d+\.$")
    SUBSECTION = re.compile(r"^\d+\.\d+$")
    SUBSUBSECTION = re.compile(r"^\d+\.\d+\.\d+$")

    @staticmethod
    def detect(lines: list[str], index: int) -> Optional[Heading]:

        line = lines[index].strip()

        # -----------------------------
        # Detect type
        # -----------------------------

        if HeadingDetector.CHAPTER.match(line):
            heading_type = "chapter"
            level = 0
            number = line

        elif HeadingDetector.ANNEXURE.match(line):
            heading_type = "annexure"
            level = 0
            number = line

        elif HeadingDetector.SUBSUBSECTION.match(line):
            heading_type = "subsubsection"
            level = 3
            number = line

        elif HeadingDetector.SUBSECTION.match(line):
            heading_type = "subsection"
            level = 2
            number = line

        elif HeadingDetector.SECTION.match(line):
            heading_type = "section"
            level = 1
            number = line

        else:
            return None
        
        ### Get title
        title = ""

        if index + 1 < len(lines):

            next_line = lines[index + 1].strip()

            # Only treat it as a title if it isn't another heading
            if (
                next_line
                and not HeadingDetector.CHAPTER.match(next_line)
                and not HeadingDetector.ANNEXURE.match(next_line)
                and not HeadingDetector.SECTION.match(next_line)
                and not HeadingDetector.SUBSECTION.match(next_line)
                and not HeadingDetector.SUBSUBSECTION.match(next_line)
            ):
                title = next_line

        return Heading(
            type=heading_type,
            level=level,
            number=number if heading_type!="section" else number.rstrip("."),
            title=title
        )