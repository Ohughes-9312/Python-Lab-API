
from contextlib import closing

import psycopg2

from src.config import DB_SETTINGS


def initialize_database():

    with closing(psycopg2.connect(**DB_SETTINGS)) as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100),
                        email VARCHAR(255)
                    )
                """)

    print("Database initialized successfully!")


if __name__ == "__main__":
    initialize_database()
