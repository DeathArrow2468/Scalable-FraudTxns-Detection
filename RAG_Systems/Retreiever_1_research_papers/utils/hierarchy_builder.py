from dataclasses import dataclass
from copy import deepcopy

from utils.heading_detector import Heading


@dataclass
class Hierarchy:

    chapter: str = ""
    chapter_title: str = ""

    section: str = ""
    section_title: str = ""

    subsection: str = ""
    subsection_title: str = ""

    subsubsection: str = ""
    subsubsection_title: str = ""


class HierarchyBuilder:

    def __init__(self):
        self.current = Hierarchy()

    def update(self, heading: Heading):

        if heading.type == "chapter":

            self.current.chapter = heading.number
            self.current.chapter_title = heading.title

            self.current.section = ""
            self.current.section_title = ""

            self.current.subsection = ""
            self.current.subsection_title = ""

            self.current.subsubsection = ""
            self.current.subsubsection_title = ""

        elif heading.type == "section":

            self.current.section = heading.number
            self.current.section_title = heading.title

            self.current.subsection = ""
            self.current.subsection_title = ""

            self.current.subsubsection = ""
            self.current.subsubsection_title = ""

        elif heading.type == "subsection":

            self.current.subsection = heading.number
            self.current.subsection_title = heading.title

            self.current.subsubsection = ""
            self.current.subsubsection_title = ""

        elif heading.type == "subsubsection":

            self.current.subsubsection = heading.number
            self.current.subsubsection_title = heading.title

    def snapshot(self):

        return deepcopy(self.current)