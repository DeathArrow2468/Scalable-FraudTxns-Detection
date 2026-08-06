from dataclasses import dataclass

@dataclass
class Hierarchy:
    chapter: str = ""
    chapter_title: str = ""
    section: str = ""
    subsection: str = ""
    heading: str = ""