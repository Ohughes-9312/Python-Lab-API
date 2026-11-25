# Python Lab API

A containerized REST API built with FastAPI and PostgreSQL using Docker, Docker Compose, VS Code Dev Containers, and WSL2.

This project was created to learn modern containerized application development from the ground up. The application provides full CRUD (Create, Read, Update, Delete) functionality for managing users while demonstrating how application containers communicate with databases through Docker networking.

---

## Features

- FastAPI REST API
- PostgreSQL database integration
- Docker Compose orchestration
- VS Code Dev Container development environment
- Interactive Swagger/OpenAPI documentation
- Full CRUD operations
- Persistent PostgreSQL data storage

---

## Architecture

The application uses a containerized architecture where API requests are processed by FastAPI and database operations are performed against PostgreSQL.

```text
API Client
(Swagger UI / HTTP Requests)
        |
        v
FastAPI Application
(Endpoints / Validation / SQL)
        |
        v
Docker Network
        |
        v
PostgreSQL Database
(Users Table / Relational Storage)
```

### Architecture Components

- **API Client:** Sends HTTP requests to interact with the API. Swagger UI provides an interactive interface for testing endpoints.
- **FastAPI Application:** Handles incoming requests, validates input data, and executes SQL queries.
- **Docker Network:** Enables communication between containerized services.
- **PostgreSQL:** Stores and manages user records in a relational database.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check whether the API is running |
| GET | `/users` | Retrieve all users |
| POST | `/users` | Create a new user |
| PUT | `/users/{user_id}` | Update an existing user |
| DELETE | `/users/{user_id}` | Delete a user |

### Create User

**Endpoint:** `POST /users`

Request body:

```json
{
  "name": "Kevin",
  "email": "kevin@example.com"
}
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

### Interactive API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Technologies Used

- Python 3.12
- FastAPI
- PostgreSQL
- psycopg2
- Docker
- Docker Compose
- VS Code Dev Containers
- WSL2
- Swagger/OpenAPI

---

## Challenges and Lessons Learned

This project involved significantly more than creating a simple API. Several real-world issues were encountered and resolved during development.

### Docker Networking

One of the most valuable lessons from this project was learning how containers communicate with each other.

Initially, the API container could not locate the PostgreSQL container because they were running on different Docker networks.

**Lesson learned:**
Containers on the same user-defined Docker network can communicate using service names and container ports.

---

### Container Persistence

Installed packages repeatedly disappeared when containers were rebuilt.

**Lesson learned:**
Changes made manually inside a running container are not a reliable way to manage application dependencies. Container rebuilds can discard those changes because the container is recreated from its image. 

Application dependencies should be declared in requirements.txt and installed during the Docker image build process through the Dockerfile.

Persistent application data, such as PostgreSQL records, should be stored using Docker volumes so that database data can survive container removal and recreation. 

### PostgreSQL Authentication

The API successfully reached PostgreSQL but failed to authenticate.

**Lesson learned:**
Database connectivity and database authentication are two separate concerns. Sucessfully connecting to a PostgreSQL container does not guarantee that the supplied username and password are valid.

Docker volumes also preserve PostgreSQL data independently of the container lifecycle. PostgreSQL initialization environment variables, such as the database username and password, are generally applied only when initializing an empty data directory. Changing these variable later does not automatically update credentials in an existing database. 

---

### FastAPI Project Structure

Import errors occurred while organizing the project into separate files.

**Lesson learned:**
Python package structure matters. Understanding modules, packages, import paths, and `__init__.py` files is essential for larger applications.

---

### Debugging Containers

Multiple issues were diagnosed using:

```bash
docker logs
docker ps
docker network inspect
docker exec
```

**Lesson learned:**
Logs are often the fastest way to identify application, networking, and dependency issues inside containers.

---

## Prerequisites

The following tools are required to run this project:

- Docker Desktop with WSL2 integration enabled
- Ubuntu on WSL2
- Visual Studio Code
- VS Code Dev Containers extension
- Git

The project uses Docker Compose to build and run the application containers.

---

## Running the Application

Build and start the containers:

```bash
docker compose up -d --build
```

Access Swagger:

```text
http://localhost:8000/docs
```

---

## Future Improvements

Planned enhancements include:

- Environment variables using `.env`
- Database migrations
- User authentication
- JWT security
- Automated testing
- GitHub Actions CI/CD
- Cloud deployment

---

## Project Outcome

Successfully designed and deployed a multi-container application consisting of:

- FastAPI API service
- PostgreSQL database
- Docker networking
- Docker Compose orchestration
- VS Code Dev Container development environment

This project provided practical experience with containerized application development, API design, database integration, debugging, and infrastructure management.