from connection import Database

def print_extensions(cur):
    print("\n========== INSTALLED EXTENSIONS ==========\n")
    cur.execute("""
        SELECT extname
        FROM pg_extension
        ORDER BY extname;
    """)
    for extension in cur.fetchall():
        print(extension[0])


def print_tables(cur):
    print("\n========== TABLES ==========\n")
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name;
    """)
    for table in cur.fetchall():
        print(table[0])


def print_row_counts(cur):

    print("\n========== ROW COUNTS ==========\n")
    tables = [
        "retriever_1_chunks",
        "retriever_2_chunks",
        "retriever_3_chunks"
    ]

    for table in tables:
        cur.execute(f"SELECT COUNT(*) FROM {table};")

        count = cur.fetchone()[0]
        print(f"{table:<25} : {count}")


def print_document_counts(cur):
    print("\n========== DOCUMENT COUNTS ==========\n")

    tables = [
        "retriever_1_chunks",
        "retriever_3_chunks"
    ]

    for table in tables:
        cur.execute(f"""
            SELECT COUNT(DISTINCT document_uuid)
            FROM {table};
        """)

        count = cur.fetchone()[0]
        print(f"{table:<25} : {count}")


def print_sample_chunk(cur):

    print("\n========== SAMPLE CHUNK ==========\n")
    cur.execute("""
        SELECT
            heading,
            LEFT(text, 200)
        FROM retriever_3_chunks
        LIMIT 1;
    """)

    row = cur.fetchone()
    if row:
        print(f"Heading : {row[0]}")
        print()
        print(row[1])

def main():
    conn = Database.connect()
    cur = conn.cursor()
    print_extensions(cur)
    print_tables(cur)
    print_row_counts(cur)
    print_document_counts(cur)
    print_sample_chunk(cur)

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()