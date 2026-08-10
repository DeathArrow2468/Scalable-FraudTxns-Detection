from pgvector.psycopg2 import register_vector
from connection import Database
from models import SearchResult

class SearchEngine:
    def __init__(self):
        self.conn = Database.connect()
        register_vector(self.conn)

        self.cur = Database.cursor(self.conn)

    def vector_search(self, table_name, embedding, top_k):

        query = f"""
        SELECT *,
               embedding <=> %s::vector AS score

        FROM {table_name}

        ORDER BY embedding <=> %s::vector

        LIMIT %s;
        """

        self.cur.execute(query, (embedding, embedding, top_k))

        results = []

        for row in self.cur.fetchall():
            metadata = dict(row)

            score = metadata.pop("score")
            text = metadata.pop("text")
            metadata.pop("embedding") # Needs to be removed for Lambda
            metadata.pop("created_at") # Needs to be removed for Lambda
            results.append(
                SearchResult(
                    text=text, score=score, metadata=metadata
                )
            )

        return results

    def close(self):
        self.cur.close()
        self.conn.close()
        