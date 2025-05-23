from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import Config

from typing import AsyncGenerator

engine = create_async_engine(url=Config.DATABASE_URL, echo=True)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    Session = sessionmaker(bind=engine,class_=AsyncSession,expire_on_commit=False)
    async with Session() as session:
        yield session




#async def init_db():
#    async with engine.begin() as conn:
#        await conn.run_sync(SQLModel.metadata.create_all)
