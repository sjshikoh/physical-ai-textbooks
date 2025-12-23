from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator
from .config import config
import logging
import ssl

logger = logging.getLogger(__name__)

# ==============================
# Async engine for Neon/PostgreSQL
# ==============================
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False  # if needed
ssl_context.verify_mode = ssl.CERT_NONE  # or CERT_REQUIRED for full verification

async_engine = create_async_engine(
    config.DATABASE_URL,
    echo=True,
    connect_args={"ssl": ssl_context},  # pass SSL here for asyncpg
)
# ==============================
# Async session factory
# ==============================
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# ==============================
# Base class for ORM models
# ==============================
Base = declarative_base()

# ==============================
# Dependency for FastAPI routes
# ==============================
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()

# ==============================
# Initialize database tables
# ==============================
async def init_db():
    logger.info("Initializing database tables...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables initialized successfully")

# ==============================
# Close database connections
# ==============================
async def close_db():
    await async_engine.dispose()
    logger.info("Database connections closed")
