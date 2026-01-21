import logging

from app import models  # noqa: F401  # ensure models are imported
from app.db.session import engine, SessionLocal
from app.factories import seed_initial_data


def init_db() -> None:
    """Create all database tables and seed initial data.

    This is called once at startup to ensure the schema exists and has
    some development data.
    """

    logging.info("[init_db] Creating database tables if they do not exist...")
    models.Base.metadata.create_all(bind=engine)
    logging.info("[init_db] Tables present: %s", list(models.Base.metadata.tables.keys()))




def init_data() -> None:
    db = SessionLocal()
    try:
        seed_initial_data(db)
    finally:
        db.close()
