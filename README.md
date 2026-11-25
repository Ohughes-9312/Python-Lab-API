# Python Lab API

A containerized REST API built with **FastAPI, PostgreSQL, Docker Compose, and Python 3.12**. This project demonstrates REST API development, relational database integration, container networking, environment-based configuration, error handling, and automated testing.

The application provides full CRUD (Create, Read, Update, Delete) functionality for managing users. It also includes structured request and response models, database error handling, and automated API tests.

---

## Features

- FastAPI REST API
- PostgreSQL database integration
- Full CRUD operations
- Docker Compose orchestration
- External Docker network integration
- Environment-based database configuration
- Pydantic request and response models
- HTTP status code handling
- Database exception logging
- Interactive Swagger/OpenAPI documentation
- Automated testing with pytest
- Mocked database testing
- VS Code Dev Container development environment
- WSL2 development workflow

---

## Architecture

The application uses a containerized architecture where API requests are processed by FastAPI and database operations are performed against PostgreSQL.

```text
API Client
(Swagger UI / HTTP Requests)
        |
        v
FastAPI Application
(Endpoints / Validation / Response Models)
        |
        v
Database Configuration
(Environment Variables)
        |
        v
Docker Network
(infrastructure_default)
        |
        v
PostgreSQL Database
(Users Table / Relational Storage)
```

### Architecture Components

- **API Client:** Sends HTTP requests to interact with the API. Swagger UI provides an interactive interface for testing endpoints.
- **FastAPI Application:** Handles incoming requests, validates input data, executes SQL queries, and returns structured responses.
- **Pydantic Models:** Define the expected structure of incoming requests and outgoing API responses.
- **Database Configuration:** Loads database connection settings from environment variables rather than hardcoding credentials.
- **Docker Network:** Enables communication between containerized services using Docker networking and service names.
- **PostgreSQL:** Stores and manages user records in a relational database.

---

## API Endpoints

| Method | Endpoint | Description | Success Status |
|---|---|---|---|
| GET | `/` | Check whether the API is running | 200 |
| GET | `/users` | Retrieve all users | 200 |
| POST | `/users` | Create a new user | 201 |
| PUT | `/users/{user_id}` | Update an existing user | 200 |
| DELETE | `/users/{user_id}` | Delete a user | 200 |

### Create User

**Endpoint:** `POST /users`

Request body:

```json
{
  "name": "Kevin",
  "email": "kevin@example.com"
}
```

Successful response:

```json
{
  "message": "User created successfully"
}
```

### Retrieve Users

**Endpoint:** `GET /users`

Example response:

```json
[
  {
    "id": 1,
    "name": "Kevin",
    "email": "kevin@example.com"
  }
]
```

### Update User

**Endpoint:** `PUT /users/{user_id}`

Request body:

```json
{
  "name": "Kevin Updated",
  "email": "kevin.updated@example.com"
}
```

### Delete User

**Endpoint:** `DELETE /users/{user_id}`

### Error Handling

The API implements HTTP status codes and error handling for common scenarios.

| Status Code | Description |
|---|---|
| 200 | Successful request |
| 201 | User successfully created |
| 404 | Requested user does not exist |
| 422 | Request validation failed |
| 500 | Database operation failed |

Database exceptions are logged internally while clients receive a generic error response.

### Interactive API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Automated Testing

The project uses **pytest** and FastAPI's `TestClient` to automate API testing.

Database interactions are mocked using Python's `unittest.mock` library. This allows endpoint behavior to be tested without modifying records in the actual PostgreSQL database.

### Test Coverage

The test suite contains 13 automated tests covering:

| Test Category | Tests |
|---|---:|
| API functionality and successful CRUD operations | 5 |
| Error handling and database failures | 3 |
| Request validation | 5 |
| **Total** | **13** |

Test scenarios include:

- API health check
- Retrieving users
- Creating users
- Updating users
- Deleting users
- Handling nonexistent user IDs
- Simulated database failures
- Missing request fields
- Invalid request data types
- Empty request bodies
- Invalid path parameters

### Running Tests

Run the test suite inside the application container:

```bash
docker compose exec app pytest -v
```

Compile the application and test files:

```bash
docker compose exec app python3 -m py_compile src/*.py tests/*.py
```

---

## Technologies Used

- Python 3.12
- FastAPI
- Pydantic
- PostgreSQL
- psycopg2
- pytest
- HTTPX2
- Python unittest.mock
- Docker
- Docker Compose
- VS Code Dev Containers
- WSL2
- Swagger/OpenAPI
- Git and GitHub

---

## Project Structure

```text
python-lab/
│
├── .devcontainer/
│   └── devcontainer.json
│
├── src/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── main.py
│   └── models.py
│
├── tests/
│   ├── __init__.py
│   └── test_api.py
│
├── .env
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

The `.env` file contains local database configuration and is excluded from version control.

---

## Environment Configuration

Database credentials and connection settings are managed through environment variables.

The application uses the following variables:

| Variable | Description |
|---|---|
| `DB_HOST` | PostgreSQL hostname |
| `DB_NAME` | Database name |
| `DB_USER` | Database username |
| `DB_PASSWORD` | Database password |
| `DB_PORT` | PostgreSQL port |

Create a local `.env` file in the project root:

```env
DB_HOST=postgres
DB_NAME=devdb
DB_USER=admin
DB_PASSWORD=your_local_database_password
DB_PORT=5432
```

Replace the example password with the password configured for your PostgreSQL database.

**Security:** Never commit `.env` or database credentials to GitHub. The application requires `DB_PASSWORD` to be set.

---

## Prerequisites

The following tools and services are required:

- Docker Desktop with WSL2 integration enabled
- Ubuntu on WSL2
- Visual Studio Code
- VS Code Dev Containers extension
- Git
- A running PostgreSQL container accessible to the application

This project connects to an existing PostgreSQL service through the external Docker network `infrastructure_default`. The network must already exist, and the PostgreSQL container must be connected to it.

The configured database, username, password, and port must match the PostgreSQL service.

---

## Running the Application

Build and start the application container:

```bash
docker compose up -d --build
```

Check the running containers:

```bash
docker compose ps
```

Check application logs:

```bash
docker compose logs app
```

Access the interactive API documentation:

```text
http://localhost:8000/docs
```

Stop the application container:

```bash
docker compose down
```

The external PostgreSQL infrastructure is managed separately from this project's Compose configuration.

---

## Challenges and Lessons Learned

This project involved significantly more than creating a simple API. Several real-world issues were encountered and resolved during development.

### Docker Networking

Initially, the API container could not locate the PostgreSQL container because they were running on different Docker networks.

**Lesson learned:**

Containers connected to the same user-defined Docker network can communicate using Docker service names and container ports. In this project, the FastAPI application connects to PostgreSQL using the database hostname `postgres` and its internal port `5432`, rather than using `localhost`.

### Container Persistence and Dependencies

Installed packages repeatedly disappeared when containers were rebuilt.

**Lesson learned:**

Changes made manually inside a running container are not a reliable way to manage application dependencies. Container rebuilds can discard those changes because the container is recreated from its image.

Application dependencies should be declared in `requirements.txt` and installed during the Docker image build process.

Development dependencies, including pytest and HTTPX2, are maintained separately in `requirements-dev.txt`.

Persistent application data, such as PostgreSQL records, should be stored using Docker volumes so that database data can survive container removal and recreation.

### PostgreSQL Authentication

The API successfully reached PostgreSQL but failed to authenticate.

**Lesson learned:**

Database connectivity and database authentication are two separate concerns. Successfully connecting to a PostgreSQL container does not guarantee that the supplied username and password are valid.

Docker volumes also preserve PostgreSQL data independently of the container lifecycle. PostgreSQL initialization environment variables are generally applied only when initializing an empty data directory. Changing these variables later does not automatically update credentials in an existing PostgreSQL database.

### Environment-Based Configuration

Database credentials were initially hardcoded in application files.

**Lesson learned:**

Centralizing database settings in a configuration module makes the application easier to maintain and reduces the risk of exposing credentials in source code.

Environment variables allow configuration to be changed without modifying application logic.

### FastAPI Project Structure

Import errors occurred while organizing the project into separate files.

**Lesson learned:**

Python package structure matters. Understanding modules, packages, import paths, and `__init__.py` files is essential for larger applications.

### API Reliability and Error Handling

The API initially lacked consistent handling for nonexistent records and database failures.

**Lesson learned:**

Appropriate HTTP status codes help API clients understand the outcome of their requests. Database exceptions should be logged for troubleshooting without exposing internal database details to clients.

### Automated Testing

Manual endpoint testing through Swagger was useful during initial development, but it was not sufficient for repeatable verification.

**Lesson learned:**

Automated tests make it easier to verify application behavior after code changes. Mocking database interactions allows endpoint logic, validation, and error handling to be tested independently of the actual database.

### Debugging Containers

Multiple issues were diagnosed using:

```bash
docker logs
docker ps
docker network inspect
docker exec
```

**Lesson learned:**

Logs and container inspection tools are essential for diagnosing application, networking, and dependency issues in containerized environments.

---

## Future Improvements

Potential enhancements include:

- Database migrations
- User authentication and authorization
- JWT-based security
- GitHub Actions CI/CD
- Cloud deployment
- Integration tests against a dedicated test database

---

## Project Outcome

Successfully designed, containerized, and tested a REST API application consisting of:

- FastAPI application service
- PostgreSQL relational database integration
- Docker networking and Compose orchestration
- Environment-based database configuration
- Structured request and response models
- CRUD operations and error handling
- Automated API testing with 13 passing tests
- Interactive Swagger/OpenAPI documentation

This project provided practical experience with Python application development, REST API design, SQL database integration, Docker networking, environment configuration, automated testing, and application debugging.
