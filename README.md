# Globant DE Challenge

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [API Documentation](#api-documentation)

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
