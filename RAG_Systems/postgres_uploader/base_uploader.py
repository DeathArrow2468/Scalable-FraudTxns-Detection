from connection import Database

class BaseUploader:
    def __init__(self):
        self.conn = Database.connect()
        self.cur = self.conn.cursor()

    def execute(self, query, params=None):
        self.cur.execute(query, params)

    def exectutemany(self, query, rows):
        self.cur.executemany(query, rows)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.cur.close()
        self.conn.close()

    def upload(self, query, rows):
        try:
            self.exectutemany(query, rows)
            self.commit()
            print(f"Uploaded {len(rows)} rows successfully.")

        except Exception:
            self.rollback()
            raise
        finally:
            self.close()

