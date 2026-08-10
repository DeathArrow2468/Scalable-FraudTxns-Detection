from dataclasses import dataclass

@dataclass
class SearchResult:
    text: str
    score: float
    metadata: dict