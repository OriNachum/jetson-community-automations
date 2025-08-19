# n8n with Postgres via Docker Compose

This project runs a self-hosted n8n instance with a persistent Postgres database using Docker and Docker Compose. Configuration is handled via an `.env` file to keep secrets out of the main compose file.

## Prerequisites

You must have Docker and Docker Compose installed and running on your system.

  - [Docker Desktop](https://www.docker.com/products/docker-desktop/) (includes Docker Compose)

## File Structure

Your project directory should contain these files before you begin:

```
.
├── docker-compose.yml
├── .env.example
└── .gitignore
```

### `docker-compose.yml`

```yaml
version: '3.7'

services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    restart: always
    ports:
      - "127.0.0.1:${N8N_PORT:-5678}:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB}
      - DB_POSTGRESDB_USER=${POSTGRES_USER}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres

  postgres:
    image: postgres:11
    restart: always
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  n8n_data:
  postgres_data:

```

### `.env.example`

This file is a template for your configuration. It should be committed to version control.

```env
# PostgreSQL Credentials - CHANGE THE PASSWORD
POSTGRES_DB=n8n
POSTGRES_USER=n8nuser
POSTGRES_PASSWORD=CHANGEME

# n8n Application Port
N8N_PORT=5678
```

### `.gitignore`

This ensures you do not accidentally commit your secrets.

```
.env
```

-----

## First-Time Setup

Follow these steps exactly.

1.  **Create Your Environment File**

    Copy the example file to a new `.env` file. This file will contain your actual secrets and will be ignored by Git.

    ```bash
    cp .env.example .env
    ```

2.  **Set Your Password**

    Open the newly created `.env` file with a text editor. Change the `POSTGRES_PASSWORD` from `CHANGEME` to a strong, unique password.

3.  **Start the Services**

    Run the following command from your terminal in the same directory as the files. Docker Compose will automatically read the `.env` file, pull the required images, and start the containers in the background.

    ```bash
    docker-compose up -d
    ```

After a minute, your n8n instance will be available at `http://localhost:5678`.

## Managing the Services

Use these commands to manage your n8n instance.

  - **Stop and remove containers:**

    ```bash
    docker-compose down
    ```

  - **Start containers:**

    ```bash
    docker-compose up -d
    ```

  - **View logs for a specific service (e.g., n8n):**

    ```bash
    docker-compose logs -f n8n
    ```

## 🚨 Security

The `.gitignore` file is configured to ignore the `.env` file. **Do not ever commit your `.env` file to a repository.** It contains your database password.

## Data Persistence

Application data is stored in Docker-managed volumes (`n8n_data` and `postgres_data`). This data persists even when the containers are stopped and removed with `docker-compose down`. To delete all data, you would need to remove the volumes manually.
