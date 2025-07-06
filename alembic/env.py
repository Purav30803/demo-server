import os
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
# Interpret the target_metadata here.
from config.database import Base  # Update with your actual models location
from models.student_model import Student 

# Update with your actual models location
target_metadata = Base.metadata
# Load environment variables from .env file
load_dotenv()

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Retrieve the DATABASE_URL from environment variables
database_url = os.getenv('DATABASE_URI')
if not database_url:
    raise ValueError("DATABASE_URL is not set in the environment.")

# Update the sqlalchemy.url dynamically
config.set_main_option('sqlalchemy.url', database_url)


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
