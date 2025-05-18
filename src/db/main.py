from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.config import db_config

engine = AsyncEngine(create_engine(url=db_config.DATABASE_URL, echo=True))


async def init_db():
    async with engine.begin() as conn:
        from src.cars.models import Cars
        from src.expenses.models import Expenses

        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session