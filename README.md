# Globant DE Challenge

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Docker Compose](#docker-compose-configuration)
- [SQL Scripts](#sql-scripts)

## Introduction

The development outlined was carried out within a dev container to solve the Globant Data Engineer exercise. The goal was to ingest CSV files through a REST API.

## Installation

To run this project locally, follow these steps:

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/IgnacioNicolasAlvarez/GlobantDE-Challenge
    ```

2. Navigate to the project directory:

    ```bash
    cd <project-directory>
    ```

3. Install the project dependencies from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the project root directory and configure the following environment variables:

    ```
    CHUNK_SIZE=1000
    SECRET_KEY=non_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
    BACKUP_BASE_PATH=/workspaces/GlobantDE/backup
    ```

    Replace the values with your specific configuration.

## API Documentation

### Upload File API

- **Endpoint:** `/uploadfile/upload/`
- **Method:** `POST`
- **Parameters:**
  - `file`: Upload a CSV file.
  - `column_names`: List of column names.
  - `sep`: Separator for the CSV file (default: `,`).
  - `is_full_load`: Whether to perform a full load (default: `True`).
  - `table_type`: Type of table (Department, etc.).

### Backup API

- **Endpoint:** `/backup/write/`
- **Method:** `POST`
- **Parameters:**
  - `table_type`: Type of table for backup (Department, etc.).

- **Endpoint:** `/backup/restore/`
- **Method:** `POST`
- **Parameters:**
  - `table_type`: Type of table for restoration (Department, etc.).
  - `date`: Date for restoration (default: today's date).

### Authentication API

- **Endpoint:** `/auth/token`
- **Method:** `POST`
- **Parameters:**
  - `username`: Username for authentication.
  - `password`: Password for authentication.

## Docker Compose Configuration

The project utilizes Docker Compose to orchestrate the following services:

- **DB (PostgreSQL Database)**: This service uses the PostgreSQL image and is responsible for managing the database. The access credentials for the database are as follows:
  - Username: `postgres`
  - Password: `postgres`
  - Database: `postgres`

- **pgAdmin**: pgAdmin is a database administration tool that runs as a separate service. It is used for managing and visualizing the PostgreSQL database. You can access pgAdmin via port `8080` on your local machine.
  - Username: `user@test.com`
  - Password: `password`

Make sure to properly configure the `.env` files and environment variables for these services to function correctly.

## SQL Scripts

The project includes a "template" folder that contains the necessary SQL scripts for performing queries. You can find various SQL scripts within this folder to interact with the PostgreSQL database.
