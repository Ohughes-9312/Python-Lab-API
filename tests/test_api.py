
from unittest.mock import MagicMock, patch

import psycopg2
from fastapi.testclient import TestClient

from src import api


client = TestClient(api.app)


# -------------------------
# DATABASE MOCK HELPER
# -------------------------

def create_mock_database(rows=None, rowcount=1):

    connection = MagicMock()
    cursor = MagicMock()

    # Simulate database connection context managers.
    connection.__enter__.return_value = connection

    # Simulate cursor context manager.
    connection.cursor.return_value = cursor
    cursor.__enter__.return_value = cursor

    # Simulate database query results.
    cursor.fetchall.return_value = rows or []
    cursor.rowcount = rowcount

    return connection, cursor


# -------------------------
# ROOT ENDPOINT
# -------------------------

def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Python Lab API Running"
    }


# -------------------------
# GET USERS
# -------------------------

def test_get_users():

    connection, cursor = create_mock_database(
        rows=[
            (1, "Kevin", "kevin@example.com"),
            (2, "Sarah", "sarah@example.com")
        ]
    )

    with patch(
        "src.api.get_db_connection",
        return_value=connection
    ):

        response = client.get("/users")

    assert response.status_code == 200

    assert response.json() == [
        {
            "id": 1,
            "name": "Kevin",
            "email": "kevin@example.com"
        },
        {
            "id": 2,
            "name": "Sarah",
            "email": "sarah@example.com"
        }
    ]

    cursor.execute.assert_called_once()


# -------------------------
# POST USER
# -------------------------

def test_create_user():

    connection, cursor = create_mock_database()

    payload = {
        "name": "John",
        "email": "john@example.com"
    }

    with patch(
        "src.api.get_db_connection",
        return_value=connection
    ):

        response = client.post("/users", json=payload)

    assert response.status_code == 201

    assert response.json() == {
        "message": "User created successfully"
    }

    cursor.execute.assert_called_once()

    assert cursor.execute.call_args[0][1] == (
        "John",
        "john@example.com"
    )


# -------------------------
# PUT USER
# -------------------------

def test_update_user():

    connection, cursor = create_mock_database(rowcount=1)

    payload = {
        "name": "Updated John",
        "email": "updated@example.com"
    }

    with patch(
        "src.api.get_db_connection",
        return_value=connection
    ):

        response = client.put("/users/1", json=payload)

    assert response.status_code == 200

    assert response.json() == {
        "message": "User updated successfully"
    }

    cursor.execute.assert_called_once()


def test_update_nonexistent_user():

    connection, cursor = create_mock_database(rowcount=0)

    payload = {
        "name": "Unknown User",
        "email": "unknown@example.com"
    }

    with patch(
        "src.api.get_db_connection",
        return_value=connection
    ):

        response = client.put("/users/9999", json=payload)

    assert response.status_code == 404

    assert response.json() == {
        "detail": "User with ID 9999 not found"
    }


# -------------------------
# DELETE USER
# -------------------------

def test_delete_user():

    connection, cursor = create_mock_database(rowcount=1)

    with patch(
        "src.api.get_db_connection",
        return_value=connection
    ):

        response = client.delete("/users/1")

    assert response.status_code == 200

    assert response.json() == {
        "message": "User deleted successfully"
    }

    cursor.execute.assert_called_once()


def test_delete_nonexistent_user():

    connection, cursor = create_mock_database(rowcount=0)

    with patch(
        "src.api.get_db_connection",
        return_value=connection
    ):

        response = client.delete("/users/9999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "User with ID 9999 not found"
    }


# -------------------------
# DATABASE ERROR HANDLING
# -------------------------

def test_database_error():

    with patch(
        "src.api.get_db_connection",
        side_effect=psycopg2.OperationalError(
            "Simulated database failure"
        )
    ):

        response = client.get("/users")

    assert response.status_code == 500

    assert response.json() == {
        "detail": "A database error occurred"
    }

# -------------------------
# REQUEST VALIDATION
# -------------------------

def test_create_user_missing_name():

    response = client.post(
        "/users",
        json={
            "email": "john@example.com"
        }
    )

    assert response.status_code == 422


def test_create_user_missing_email():

    response = client.post(
        "/users",
        json={
            "name": "John"
        }
    )

    assert response.status_code == 422


def test_create_user_invalid_data_types():

    response = client.post(
        "/users",
        json={
            "name": 123,
            "email": "john@example.com"
        }
    )

    assert response.status_code == 422


def test_create_user_empty_body():

    response = client.post("/users")

    assert response.status_code == 422


def test_update_user_invalid_id():

    response = client.put(
        "/users/invalid",
        json={
            "name": "John",
            "email": "john@example.com"
        }
    )

    assert response.status_code == 422
