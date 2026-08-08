import uuid
from pathlib import Path

CATEGORY_MAP = {
    "RBI": "Regulation",
    "NPCI": "Payment Network",
    #"CERT-IN": "Cyber Security",
    #"FIU": "AML",
    "Razorpay": "Industry",
    "National Insurance": "Industry"
}

def build_metadata(file_path: Path, total_pages: int):
    authority = file_path.parent.name

    return {
        "document_uuid": str(uuid.uuid4()),
        "document_id": file_path.stem.upper().replace(" ", "_"),
        "title": file_path.stem.replace("_", " "),
        "authority": authority,
        "category": CATEGORY_MAP.get(authority, "Other"),
        "source_file": str(file_path),
        "file_type": file_path.suffix.replace(".", ""),
        "version": "1.0",
        "year": None,
        "total_pages": total_pages
    }