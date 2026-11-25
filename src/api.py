import logging
from contextlib import closing
from functools import wraps

from fastapi import FastAPI, HTTPException, status
import psycopg2

from src.config import DB_SETTINGS
from src.models import User, UserResponse, MessageResponse


# -------------------------
# APPLICATION CONFIGURATION
# -------------------------

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

app = FastAPI()


# -------------------------
# DATABASE CONNECTION HELPER
# -------------------------

def handle_database_errors(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            return func(*args, **kwargs)

        except psycopg2.Error:
            logger.exception("Database operation failed")

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="A database error occurred"
            )

    return wrapper


def get_db_connection():
    return closing(
        psycopg2.connect(**DB_SETTINGS)
    )


# -------------------------
# API ENDPOINTS
# -------------------------

@app.get("/")
def root():
    return {"message": "Python Lab API Running"}


@app.get(
    "/users",
    response_model=list[UserResponse]
)
@handle_database_errors
def get_users():

    with get_db_connection() as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, name, email
                    FROM users
                    ORDER BY id
                """)

                rows = cur.fetchall()

    return [
        {
            "id": row[0],
            "name": row[1],
            "email": row[2]
        }
        for row in rows
    ]


@app.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=MessageResponse
)
@handle_database_errors
def create_user(user: User):

    with get_db_connection() as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users (name, email)
                    VALUES (%s, %s)
                    """,
                    (user.name, user.email)
                )

    return {"message": "User created successfully"}


@app.put(
    "/users/{user_id}",
    response_model=MessageResponse
)
@handle_database_errors
def update_user(user_id: int, user: User):

    with get_db_connection() as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE users
                    SET name = %s,
                        email = %s
                    WHERE id = %s
                    """,
                    (user.name, user.email, user_id)
                )

                if cur.rowcount == 0:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with ID {user_id} not found"
                    )

    return {"message": "User updated successfully"}


@app.delete(
    "/users/{user_id}",
    response_model=MessageResponse
)
@handle_database_errors
def delete_user(user_id: int):

    with get_db_connection() as conn:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM users
                    WHERE id = %s
                    """,
                    (user_id,)
                )

                if cur.rowcount == 0:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with ID {user_id} not found"
                    )

    return {"message": "User deleted successfully"}