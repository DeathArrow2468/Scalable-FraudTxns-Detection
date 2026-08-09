from connection import Database

TABLES = [
    "retriever_1_chunks",
    "retriever_2_chunks",
    "retriever_3_chunks"
]

conn = Database.connect()
cur = conn.cursor()

for table in TABLES:
    cur.execute(f"TRUNCATE TABLE {table};")
    print(f"Truncated {table}")

conn.commit()

cur.close()
conn.close()

print("All tables reset successfully.")