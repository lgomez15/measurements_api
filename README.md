# Measurement API

A FastAPI-based API for managing measurement objects with PostgreSQL persistence. This API allows users to perform CRUD (Create, Read, Update, Delete) operations on measurement data, which includes attributes such as `co2_value`, `unit`, `source`, and `description`.

## Table of Contents
- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Future Improvements](#future-improvements)

## Overview
The Measurement API is built using FastAPI and uses PostgreSQL as the database to store measurement data. Each measurement object contains the following attributes:
- `co2_value` (required, numeric): The CO2 value of the measurement.
- `unit` (optional, string): The unit of measurement (e.g., "ppm").
- `source` (optional, string): The source of the measurement (e.g., "sensor1").
- `description` (optional, string): Additional description of the measurement.

The API supports full CRUD operations, allowing users to create, retrieve, update, and delete measurements. Request validation and error handling are implemented using Pydantic and FastAPI's built-in features.

## Prerequisites
To run this application, you need the following installed:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.10 or higher

## Setup
1. **Clone the repository** (if applicable):
   ```bash
   git clone <repository-url>
   cd measurement-api
   ```

2. **Environment Configuration**:
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Adjust the `.env` file if necessary (e.g., database credentials). The default configuration should work for most setups.

3. **Build and Run the Application**:
   - Use Docker Compose to build and start the application:
     ```bash
     docker-compose up --build
     ```
   - This command will build the Docker image, start the PostgreSQL database, and run the FastAPI application.

## Running the Application
- The API will be available at `http://localhost:8000`.
- Access the automatically generated Swagger documentation at `http://localhost:8000/docs` to explore and test the API endpoints interactively.

## API Endpoints
The following endpoints are available for interacting with the measurement data:

- **POST /measurements/**: Create a new measurement.
  - Request body: JSON object with `co2_value`, `unit`, `source`, and `description`.
  - Response: The created measurement object with an assigned `id` and `created_at` timestamp.

- **GET /measurements/**: Retrieve a list of all measurements.
  - Supports pagination with `skip` and `limit` query parameters (default: `skip=0`, `limit=100`).

- **GET /measurements/{id}**: Retrieve a specific measurement by its ID.
  - Returns the measurement if found, otherwise returns a 404 error.

- **PUT /measurements/{id}**: Update an existing measurement by its ID.
  - Request body: JSON object with fields to update (e.g., `co2_value`, `description`).
  - Response: The updated measurement object.

- **DELETE /measurements/{id}**: Delete a measurement by its ID.
  - Returns 204 No Content if successful, otherwise 404 if the measurement is not found.

## Testing
The project includes integration tests to verify the functionality of the API. To run the tests:
```bash
docker-compose exec app pytest
```
This command will execute all tests located in the `app/tests/` directory using `pytest`.

## Project Structure
The project is organized as follows:
```
measurement-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # Database configuration and session management
│   ├── models/                 # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── measurement.py      # Measurement model definition
│   ├── schemas/                # Pydantic schemas for request/response validation
│   │   ├── __init__.py
│   │   └── measurement.py      # Measurement schemas
│   ├── routes/                 # API route definitions
│   │   ├── __init__.py
│   │   └── measurement.py      # Measurement CRUD routes
│   ├── dependencies.py         # Dependency injections (e.g., database session)
│   └── tests/                  # Integration tests
│       ├── __init__.py
│       ├── conftest.py         # Pytest fixtures
│       └── test_measurement.py # Tests for measurement endpoints
├── Dockerfile                  # Docker configuration for the application
├── docker-compose.yml          # Docker Compose configuration for app and database
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
└── .env.example                # Example environment variables
```

## Future Improvements
While the current implementation meets the basic requirements, several enhancements could be considered for future development:
- **Authentication and Authorization**: Add user authentication (e.g., JWT, OAuth2) to secure the API and restrict access to certain operations.
- **Pagination**: Implement more advanced pagination for the `GET /measurements/` endpoint, including support for sorting and filtering.
- **Additional Validation**: Enhance validation for measurement attributes, such as ensuring `co2_value` is within a realistic range or that `unit` is one of a predefined set of values.
- **Database Migrations**: Replace the current `create_all` approach with migrations using Alembic for better schema management in larger projects.
- **Kafka Integration**: Consider integrating with Kafka for real-time data processing and event-driven architecture.
- **Asynchronous Support**: Explore the use of asynchronous database drivers (e.g., asyncpg) for improved performance under high load.
