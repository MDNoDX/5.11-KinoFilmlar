from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DB_URL = 'sqlite+aiosqlite:///./films.db'
engine = create_async_engine(DB_URL)
LocalSession = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with LocalSession() as session:
        yield session

class Base(DeclarativeBase):
    pass