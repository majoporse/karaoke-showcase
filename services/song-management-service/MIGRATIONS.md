# Database Migrations with Alembic

This guide explains how to create, manage, and apply database migrations in the Song Management Service using Alembic.

## Overview

Alembic is a lightweight database migration tool for SQLAlchemy that enables version control for your database schema. All migrations are tracked in the `alembic/versions/` directory and can be applied in order to any database.

## Configuration

The migration setup is configured in `alembic.ini` and `alembic/env.py`:

- **alembic.ini** - Main configuration file (database URL, logging, etc.)
- **alembic/env.py** - Migration environment configuration (handles async SQLAlchemy)
- **alembic/versions/** - Directory containing all migration scripts

The service uses PostgreSQL with async SQLAlchemy. The `env.py` file automatically converts the async connection string to a sync one for Alembic compatibility.

## Prerequisites

Ensure your environment variables are set:

```bash
export DATABASE_URL="postgresql+asyncpg://postgres:password@localhost:5432/karaoke_db"
```

The migration system will automatically convert this to a sync PostgreSQL connection for Alembic operations.

## Initializing Alembic

If you're setting up Alembic for a new project, follow these steps:

### 1. Install Alembic

```bash
uv pip install alembic
```

Or add it to your `requirements.txt` or `pyproject.toml`:

```bash
uv sync
```

### 2. Initialize Alembic

Create the Alembic environment in your project:

```bash
uv run alembic init alembic
```

This creates:
- `alembic/` - Migration directory
- `alembic/versions/` - Folder for migration scripts
- `alembic/env.py` - Migration environment configuration
- `alembic/script.py.mako` - Migration template
- `alembic.ini` - Alembic configuration file

### 3. Configure Database Connection

Edit `alembic/env.py` to set up your database:

```python
import os
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from alembic import context
from infrastructure.models.base import Base

# Load environment variables
load_dotenv()

config = context.config
target_metadata = Base.metadata

# Get DATABASE_URL from environment
database_url = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/karaoke_db",
)
# Convert asyncpg to psycopg for Alembic (sync operations)
DATABASE_URL = database_url.replace("postgresql+asyncpg://", "postgresql://")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section) or {}
    configuration["sqlalchemy.url"] = DATABASE_URL
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 4. Configure alembic.ini

Update `alembic.ini` with your settings:

```ini
[alembic]
script_location = ./alembic
sqlalchemy.url = 

[post_write_hooks]
# Optional: format migrations with Black
hooks = black
black.type = console_scripts
black.entrypoint = black
black.options = -l 79 REVISION_SCRIPT_FILENAME
```

### 5. Create Initial Migration

Generate the first migration based on your models:

```bash
uv run alembic revision --autogenerate -m "initial schema"
```

This detects all your SQLAlchemy models and creates a migration to set up the database schema.

### 6. Apply Initial Migration

```bash
uv run alembic upgrade head
```

Your database schema is now version controlled with Alembic!

## Creating Migrations

### Auto-generate Migrations

The recommended approach is to auto-generate migrations based on model changes:

```bash
# Generate a migration for model changes
uv run alembic revision --autogenerate -m "descriptive message"
```

**Example:**
```bash
uv run alembic revision --autogenerate -m "add_index_to_lyrics_table"
```

This will create a new migration file in `alembic/versions/` with:
- Detected schema changes (added columns, tables, indexes, etc.)
- Upgrade function (applies the changes)
- Downgrade function (reverts the changes)

### Manual Migrations

For complex changes not detected by auto-generation:

```bash
# Create an empty migration file
uv run alembic revision -m "complex schema change"
```

Then edit the generated file in `alembic/versions/` to add your custom SQL operations:

```python
def upgrade() -> None:
    """Upgrade schema - add custom logic here."""
    op.create_table(
        'new_table',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    """Downgrade schema - reverse the changes."""
    op.drop_table('new_table')
```

## Migration Workflow

### 1. Make Model Changes

Update your SQLAlchemy models in `infrastructure/models/`:

```python
class Lyrics(Base):
    __tablename__ = "lyrics"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    full_text = Column(String, nullable=False)
    # Add new column
    source = Column(String(50), nullable=True)  # New column
```

### 2. Generate Migration

```bash
uv run alembic revision --autogenerate -m "add_source_column_to_lyrics"
```

Alembic will detect the new column and create an appropriate migration.

### 3. Review Generated Migration

Always review the generated migration file:

```bash
cat alembic/versions/<timestamp>_add_source_column_to_lyrics.py
```

Ensure the upgrade and downgrade functions are correct.

### 4. Apply Migration

```bash
# Apply the latest migration
uv run alembic upgrade head

# Apply a specific migration
uv run alembic upgrade <revision_id>

# Apply n migrations
uv run alembic upgrade +2
```

### 5. Verify Changes

Connect to your database and verify the schema changes:

```bash
psql -U postgres -d karaoke_db -c "\d lyrics"
```

## Common Commands

### Check Migration Status

```bash
# Show current database revision
uv run alembic current

# Show all revisions (history and branches)
uv run alembic branches

# Show migration log
uv run alembic history

# Show detailed history with SQL
uv run alembic history --verbose
```

### Apply Migrations

```bash
# Apply all pending migrations to head
uv run alembic upgrade head

# Apply next 1 migration
uv run alembic upgrade +1

# Apply next 2 migrations
uv run alembic upgrade +2

# Downgrade to specific revision
uv run alembic downgrade <revision_id>

# Downgrade one step
uv run alembic downgrade -1

# Downgrade all migrations (careful!)
uv run alembic downgrade base
```

### Detect Schema Changes

```bash
# Show what Alembic would autogenerate (dry run)
uv run alembic upgrade head --sql

# Generate new migration without applying
uv run alembic revision --autogenerate -m "message"
```

## Migration File Structure

Each migration file contains:

```python
"""Description of the change

Revision ID: <unique_id>
Revises: <parent_revision_id>
Create Date: <timestamp>

"""

from alembic import op
import sqlalchemy as sa

revision: str = "<unique_id>"
down_revision: str | None = "<parent_revision_id>"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    """Apply the schema changes."""
    # Add/modify tables, columns, indexes, constraints, etc.
    pass


def downgrade() -> None:
    """Revert the schema changes."""
    # Reverse all changes from upgrade()
    pass
```

## Best Practices

### 1. Descriptive Messages

Use clear, concise migration names that describe the change:

```bash
# Good ✓
uv run alembic revision --autogenerate -m "add_confidence_score_to_lyrics"
uv run alembic revision --autogenerate -m "create_index_on_processing_results_youtube_id"

# Avoid ✗
uv run alembic revision --autogenerate -m "fix"
uv run alembic revision --autogenerate -m "update"
```

### 2. One Change Per Migration

Keep migrations focused on a single logical change:

```bash
# Good - separate migrations
uv run alembic revision --autogenerate -m "add_source_column_to_lyrics"
uv run alembic revision --autogenerate -m "create_index_on_source"

# Avoid - multiple unrelated changes
uv run alembic revision --autogenerate -m "add_source_and_fix_constraint"
```

### 3. Always Include Downgrade

Write downgrade functions that completely reverse the upgrade:

```python
def upgrade() -> None:
    op.add_column('lyrics', sa.Column('source', sa.String(50)))

def downgrade() -> None:
    op.drop_column('lyrics', 'source')
```

### 4. Test Migrations Locally

Always test migrations before deploying:

```bash
# Apply migration
uv run alembic upgrade head

# Verify changes
psql -U postgres -d karaoke_db -c "\d"

# Test downgrade
uv run alembic downgrade -1

# Test upgrade again
uv run alembic upgrade head
```

### 5. Review Generated SQL

Always review auto-generated migrations for accuracy:

```bash
# View SQL that would be executed
uv run alembic upgrade head --sql

# Apply with verification
uv run alembic upgrade head
```

## Troubleshooting

### Issue: "Target database is not up to date"

The migration revision table is out of sync. Check the current revision:

```bash
uv run alembic current
```

### Issue: Migration fails to apply

1. Check the error message carefully
2. Review the migration file for syntax errors
3. Verify the database connection with `uv run alembic current`
4. Test with a backup database first

### Issue: "alembic: No such file or directory"

Ensure you're in the correct directory:

```bash
cd /path/to/song-management-service
uv run alembic --version
```

### Issue: Can't detect model changes

Make sure models are imported in `alembic/env.py`:

```python
# This is already configured, but verify:
from infrastructure.models.base import Base

target_metadata = Base.metadata
```

## Deployment

### Development

```bash
# In development, apply migrations before running the service
uv run alembic upgrade head
uv run python main.py
```

### Docker

Migrations are applied automatically in the Docker Compose setup via the `docker-compose.yml` configuration.

### CI/CD

Add migration validation to your CI/CD pipeline:

```bash
# Check if migrations are up to date
uv run alembic upgrade head --sql

# Verify no pending migrations
uv run alembic current
```

## Advanced Topics

### Branching Migrations

For concurrent feature development, you can create branches:

```bash
uv run alembic branch --rev-id=<base_revision> feature_branch
```

### Multiple Databases

If you need to manage migrations for multiple databases, use:

```bash
uv run alembic upgrade head -x database=primary
```

### Custom Migration Logic

Add custom Python logic in migrations:

```python
def upgrade() -> None:
    op.add_column('lyrics', sa.Column('processed', sa.Boolean(), default=False))
    
    # Custom logic
    op.execute('''
        UPDATE lyrics SET processed = true
        WHERE confidence_score > 0.8
    ''')

def downgrade() -> None:
    op.drop_column('lyrics', 'processed')
```

## Resources

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)
- [Database Versioning Best Practices](https://www.liquibase.org/get-started/best-practices)
