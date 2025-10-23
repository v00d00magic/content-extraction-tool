from Objects.Object import Object
from peewee import Database
from typing import Any
from pydantic import Field

class ConnectionWrapper(Object):
    name: str = Field()
    db: Any = Field()

    def create(self, items: list):
        for item in items:
            item.setClsDB(self.db)
            item.setClsTableName(item.table_name)

        self.db.create_tables(items)
