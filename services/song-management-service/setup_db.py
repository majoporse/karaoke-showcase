#!/usr/bin/env python3
import os
import sys
from urllib.parse import urlparse
from dotenv import load_dotenv
import psycopg2
from alembic.config import Config
from alembic import command

load_dotenv()

def create_database_if_not_exists():
    """Create the database if it doesn't exist."""
    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:password@localhost:5432/karaoke_db",
    )
    # Parse the URL to get connection parameters
    parsed = urlparse(database_url.replace("+asyncpg", ""))

    db_name = parsed.path.lstrip("/")
    db_user = parsed.username or "postgres"
    db_password = parsed.password or "password"
    db_host = parsed.hostname or "localhost"
    db_port = parsed.port or 5432

    # Connect to default 'postgres' database to create the target database
    conn = psycopg2.connect(
        dbname="postgres",
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Check if database exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
    exists = cur.fetchone()

    if not exists:
        print(f"Creating database '{db_name}'...")
        cur.execute(f'CREATE DATABASE "{db_name}"')
        print(f"Database '{db_name}' created.")
    else:
        print(f"Database '{db_name}' already exists.")

    cur.close()
    conn.close()


def run_alembic_migrations():
    """Generate and apply Alembic migrations."""
    print("Running Alembic migrations...")

    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    alembic_ini = os.path.join(script_dir, "alembic.ini")

    # Configure Alembic
    config = Config(alembic_ini)

    # Generate initial migration
    print("Generating initial migration...")
    command.revision(config, autogenerate=True, message="initial_schema")

    # Apply migrations
    print("Applying migrations...")
    command.upgrade(config, "head")

    print("Migrations complete!")


if __name__ == "__main__":
    try:
        create_database_if_not_exists()
        run_alembic_migrations()
        print("\nDatabase setup complete!")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
