import sqlite3


class DBManager:

    def __init__(self):

        self.conn = sqlite3.connect(
            "words.db"
        )

        self.cursor = self.conn.cursor()

        self.create_table()

    def create_table(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            content TEXT NOT NULL,

            hint TEXT NOT NULL,

            difficulty INTEGER DEFAULT 1
        )
        """)

        self.conn.commit()

    def insert_word(
        self,
        content,
        hint,
        difficulty
    ):

        self.cursor.execute(
            """
            INSERT INTO words
            (
                content,
                hint,
                difficulty
            )
            VALUES
            (?, ?, ?)
            """,
            (
                content,
                hint,
                difficulty
            )
        )

        self.conn.commit()

    def get_random_word(self):

        self.cursor.execute(
            """
            SELECT
                content,
                hint,
                difficulty
            FROM words
            ORDER BY RANDOM()
            LIMIT 1
            """
        )

        return self.cursor.fetchone()

    def close(self):

        self.conn.close()