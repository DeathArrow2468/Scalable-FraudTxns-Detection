import json
from pathlib import Path

from base_uploader import BaseUploader

EMBEDDINGS_FOLDER = Path(r"C:\Users\Manav\OneDrive\Desktop\FraudTranactionDetection\RAG_Systems\Retriever_3_docs_on_guidelines\embeddings")


INSERT_QUERY = """
INSERT INTO retriever_3_chunks(
    chunk_uuid,
    document_uuid,
    authority,
    document_title,
    chapter,
    chapter_title,
    section,
    subsection,
    heading,
    page_start,
    page_end,
    text,
    embedding_text,
    embedding
)
VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
);
"""

def parse_documents(collection):
    rows = []

    for chunk in collection["chunks"]:
        meta = chunk["metadata"]
        rows.append(
            (
                meta["chunk_uuid"],
                meta["document_uuid"],

                meta["authority"],
                meta["document_title"],

                meta["chapter"],
                meta["chapter_title"],

                meta["section"],
                meta["subsection"],

                meta["heading"],

                meta["page_start"],
                meta["page_end"],

                chunk["text"],
                chunk["embedding_text"],

                chunk["embedding"]
            )
        )

    return rows

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def upload_folder(folder):

    for file in Path(folder).rglob("*.json"):
        uploader = BaseUploader()
        collection = load_json(file)

        rows = parse_documents(collection)

        print(f"Uploading file: {file.name}")
        uploader.upload(INSERT_QUERY, rows)
        print(f"Successfully uploaded rows from: {file.name}")


if __name__ == "__main__":
    # collection = load_json(next(Path(EMBEDDINGS_FOLDER).rglob("*.json")))

    # print(type(collection["chunks"][0]["embedding"]))

    # print(len(collection["chunks"][0]["embedding"]))

    #print(len(collection["chunks"]))
    upload_folder(EMBEDDINGS_FOLDER)
