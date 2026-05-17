"""Schema management for Tuttle databases.

During development the SQLModel class definitions in model.py are the single
source of truth.  We simply call ``create_all`` which creates any missing
tables (and is a no-op for tables that already exist).

For destructive schema changes, delete the ``.db`` file first — the existing
``reset_database()`` flow already does this.
"""

from loguru import logger
from sqlalchemy import create_engine
from sqlmodel import SQLModel

import tuttle.model  # noqa: F401 — ensure all table classes are registered


def ensure_schema(db_url: str) -> None:
    """Create all tables defined by SQLModel if they don't already exist."""
    engine = create_engine(db_url)
    try:
        SQLModel.metadata.create_all(engine)
        logger.debug(f"Schema ensured for {db_url}")
    finally:
        engine.dispose()
