import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

class TableMerger:
    def __init__(self, db_url):
        self.engine = create_async_engine(db_url)

    async def merge_tables(self, table1_name, table2_name):
        async with self.engine.connect() as conn:
            result = await conn.execute(text(f"PRAGMA table_info({table1_name})"))
            columns = [row[1] for row in result]

            result = await conn.execute(text(f"PRAGMA table_info({table2_name})"))
            existing_columns = [row[1] for row in result]
            new_columns = [col for col in columns if col not in existing_columns]

            for column in new_columns:
                await conn.execute(text(f"ALTER TABLE {table2_name} ADD COLUMN {column} VARCHAR NOT NULL"))

            insert_query = text(f"INSERT INTO {table2_name} ({', '.join(columns)}) SELECT {', '.join(columns)} FROM {table1_name}")
            await conn.execute(insert_query)

async def main():
    merger = TableMerger('sqlite+aiosqlite:///test.db')
    await merger.merge_tables('table_2', 'table_1')

if __name__ == '__main__':
    asyncio.run(main())
