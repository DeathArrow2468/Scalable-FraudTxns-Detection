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
    def _is_heading(line: str) -> bool:

        return (
            HeadingDetector.CHAPTER.match(line)
            or HeadingDetector.ANNEXURE.match(line)
            or HeadingDetector.SECTION.match(line)
            or HeadingDetector.SUBSECTION.match(line)
            or HeadingDetector.SUBSUBSECTION.match(line)
        )

    @staticmethod
    def detect(lines: list[str], index: int) -> Optional[Heading]:

        line = lines[index].strip()

        if not line:
            return None

        # ------------------------
        # RBI style headings
        # ------------------------

        if HeadingDetector.CHAPTER.match(line):
            return Heading(
                type="chapter",
                level=0,
                number=line,
                title=lines[index + 1] if index + 1 < len(lines) else ""
            )

        if HeadingDetector.ANNEXURE.match(line):
            return Heading(
                type="annexure",
                level=0,
                number=line,
                title=lines[index + 1] if index + 1 < len(lines) else ""
            )

        if HeadingDetector.SUBSUBSECTION.match(line):
            return Heading(
                type="subsubsection",
                level=3,
                number=line,
                title=lines[index + 1] if index + 1 < len(lines) else ""
            )

        if HeadingDetector.SUBSECTION.match(line):
            return Heading(
                type="subsection",
                level=2,
                number=line,
                title=lines[index + 1] if index + 1 < len(lines) else ""
            )

        if HeadingDetector.SECTION.match(line):
            return Heading(
                type="section",
                level=1,
                number=line.rstrip("."),
                title=lines[index + 1] if index + 1 < len(lines) else ""
            )

        # ------------------------
        # Generic document headings
        # ------------------------

        # Single reasonably short line
        if (
            len(line) < 120
            and not line.endswith(".")
            and ":" not in line
        ):

            # next line exists
            if index + 1 < len(lines):

                nxt = lines[index + 1].strip()

                # next line should NOT itself be a heading
                if (
                    nxt
                    and not HeadingDetector._is_heading(nxt)
                    and len(nxt) > len(line)
                ):

                    return Heading(
                        type="generic",
                        level=1,
                        number="",
                        title=line
                    )

        return None