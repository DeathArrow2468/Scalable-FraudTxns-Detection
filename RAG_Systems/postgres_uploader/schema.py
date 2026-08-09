from connection import Database

def create_extension(cur):
    cur.execute("""
    CREATE EXTENSION IF NOT EXISTS vector;
    """)

def create_retriever1(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS retriever_1_chunks(
        chunk_uuid TEXT PRIMARY KEY,
        document_uuid TEXT,
        paper_title TEXT,
        fraud_pattern TEXT,
        heading TEXT,
        text TEXT,
        embedding_text TEXT,
        embedding vector(1024),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

def create_retriever2(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS retriever_2_chunks(
        feature_name TEXT PRIMARY KEY,
        description TEXT,
        examples TEXT,
        embedding_text TEXT,
        embedding vector(1024),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

def create_retriever3(cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS retriever_3_chunks(
        chunk_uuid TEXT PRIMARY KEY,
        document_uuid TEXT,
        authority TEXT,
        document_title TEXT,
        chapter TEXT,
        chapter_title TEXT,
        section TEXT,
        subsection TEXT,
        heading TEXT,
        page_start INTEGER,
        page_end INTEGER,
        text TEXT,
        embedding_text TEXT,
        embedding vector(1024),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

def main():
    conn = Database.connect()

    cur = conn.cursor()
    create_extension(cur)
    create_retriever1(cur)
    create_retriever2(cur)
    create_retriever3(cur)

    conn.commit()

    cur.close()
    conn.close()

    print('Schema made successfully')

if __name__ == "__main__":
    main()