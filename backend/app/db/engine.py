"""SQLAlchemy engine: the app's single entry point to the database.

An Engine owns a *connection pool*. Opening a Postgres connection is expensive (TCP handshake,
authentication, session setup), so the pool keeps a few open and lends them out per request.
Creating an Engine does NOT connect; the first connection happens on first use. That keeps
create_app() free of side effects.
"""

import logging

from sqlalchemy import Engine, create_engine, make_url, text
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

# Seconds to wait for Postgres to accept a connection before giving up. Without this, a
# health check against a dead database could hang for a long time.
CONNECT_TIMEOUT_SECONDS = 2


def build_engine(database_url: str) -> Engine:
    connect_args: dict[str, object] = {}
    if make_url(database_url).get_backend_name() == "postgresql":
        connect_args["connect_timeout"] = CONNECT_TIMEOUT_SECONDS

    return create_engine(
        database_url,
        # Before lending out a pooled connection, check it's still alive. Connections can die
        # silently (DB restart, network blip); this swaps a dead one for a fresh one.
        pool_pre_ping=True,
        connect_args=connect_args,
    )


def database_is_reachable(engine: Engine) -> bool:
    """Run the cheapest possible query. True only if the DB accepted a connection and answered."""
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        logger.warning("Database health check failed", exc_info=True)
        return False
    return True
