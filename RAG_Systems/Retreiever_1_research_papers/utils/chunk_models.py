from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ChunkMetadata:
    chunk_uuid: str
    document_uuid: str
    chunk_index: int

    authority: str
    document_title: str

    chapter: str
    chapter_title: str

    section: str
    subsection: str

    heading: str

    page_start: int
    page_end: int

@dataclass
class Chunk:
    metadata: ChunkMetadata
    text: str
    embedding: Optional[List[float]] = None
    embedding_text: Optional[List[str]] = None

@dataclass
class ChunkCollection:
    document_uuid: str
    chunks: List[Chunk] = field(default_factory=list)