from dataclasses import dataclass, field
from typing import List


@dataclass
class Page:

    page_number: int

    text: str


@dataclass
class Paper:

    title: str

    pages: List[Page] = field(default_factory=list)