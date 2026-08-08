from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class DocumentMetadata:
    document_uuid: str
    document_id: str
    title: str
    authority: str
    category: str
    source_file: str
    file_type: str
    version: str
    year: Optional[int]
    total_pages: int

@dataclass
class Page: 
    page_number: int
    text: str
    char_count: int

@dataclass
class Document:
    metadata: DocumentMetadata
    pages: List[Page] = field(default_factory=list)