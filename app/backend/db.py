from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase



class Base(DeclarativeBase):
    pass

DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@db:5432/prodapi'
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)