from fastapi import FastAPI
import psycopg2
from src.models import User

app = FastAPI()

DB_SETTINGS = {
    "host": "postgres",
    "database": "devdb",
    "user": "admin",
    "password": "***REMOVED***",
    "port": "5432"
}

@app.get("/")
def root():
    return {"message": "Python Lab API Running"}

@app.get("/users")
def get_users():

    conn = psycopg2.connect(**DB_SETTINGS)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email
        FROM users
        ORDER BY id
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "email": row[2]
        }
        for row in rows
    ]

from src.models import User

@app.post("/users")
def create_user(user: User):

    conn = psycopg2.connect(**DB_SETTINGS)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users (name, email)
        VALUES (%s, %s)
        """,
        (user.name, user.email)
    )

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "User created successfully"
    }


@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):

    conn = psycopg2.connect(**DB_SETTINGS)
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET name = %s,
            email = %s
        WHERE id = %s
        """,
        (user.name, user.email, user_id)
    )

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "User updated"
    }


@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    conn = psycopg2.connect(**DB_SETTINGS)
    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM users
        WHERE id = %s
        """,
        (user_id,)
    )

    conn.commit()

    cur.close()
    conn.close()

    return {
        "message": "User deleted"
    }