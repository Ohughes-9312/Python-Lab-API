import psycopg2

conn = psycopg2.connect(
    host="postgres",
    database="devdb",
    user="admin",
    password="***REMOVED***",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255)
)
""")

cur.execute(
    """
    INSERT INTO users (name, email)
    VALUES (%s, %s)
    """,
    ("Kevin", "kevin@example.com")
)

conn.commit()

print("✅ User inserted!")

cur.close()
conn.close()