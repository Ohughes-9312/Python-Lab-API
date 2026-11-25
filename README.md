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

```text
Browser
   ↓
Swagger UI
   ↓
FastAPI
   ↓
Python Application
   ↓
Docker Network
   ↓
PostgreSQL
```

---

## Endpoints

### Users

| Method | Endpoint | Description |
|----------|----------|-------------|
| GET | /users | Retrieve all users |
| POST | /users | Create a user |
| PUT | /users/{user_id} | Update a user |
| DELETE | /users/{user_id} | Delete a user |

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
Containers communicate through Docker networks, not through localhost. Proper network configuration is required for inter-container communication.

---

### Container Persistence

Installed packages repeatedly disappeared when containers were rebuilt.

**Lesson learned:**
Anything installed manually inside a running container is temporary. Dependencies must be stored inside `requirements.txt` and installed during the image build process.

This led to improving the Dockerfile to automatically install application dependencies.

---

### PostgreSQL Authentication

The API successfully reached PostgreSQL but failed to authenticate.

**Lesson learned:**
Docker volumes persist data even when containers are removed. Database initialization variables are only applied during the initial database creation process.

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