import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase


engine = create_async_engine("sqlite+aiosqlite:///test.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
    pass

class Table1(Model):
    __tablename__ = 'table_1'

    field1: Mapped[int] = mapped_column(primary_key=True)
    field2: Mapped[str]
    field3: Mapped[str]

class Table2(Model):
    __tablename__ = 'table_2'

    field1: Mapped[int] = mapped_column(primary_key=True)
    field2: Mapped[str]
    field3: Mapped[str]
    field4: Mapped[str]
    field5: Mapped[str]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)

async def main():
    await create_tables()

if __name__ == '__main__':
    asyncio.run(main())
