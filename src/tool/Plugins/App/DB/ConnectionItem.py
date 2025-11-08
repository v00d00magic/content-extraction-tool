from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase, DatabaseProxy, Database
from Objects.Object import Object
from Plugins.Data.Text import Text
from pathlib import Path
from pydantic import Field
from typing import Any
from enum import Enum
from App import app

class ConnectionEnum(Enum):
    sqlite = "sqlite"

class ConnectionItem(Object):
    name: str = Field()
    display_name: str = Field(default = None)

    protocol: ConnectionEnum = Field(default=ConnectionEnum.sqlite)
    data: str = Field(default=None)
    directory: str = Field(default='?cwd?/storage/common_storage')

    db: Any = None # Database

    def connect(self) -> Database:
        db = None

        match(self.protocol.value):
            case ConnectionEnum.sqlite.value:
                if self.data == None:
                    db_dir = Path(app.Storage.get('dbs').dir()).joinpath(self.name)
                    db_dir.mkdir(exist_ok=True)

                    self.data = str(db_dir.joinpath('items.db'))
                    self.directory = str(db_dir)

                text = Text.use(
                    text = self.data
                )
                text.replaceCwd()
                db = SqliteDatabase(text.content.text)

        return db

    def getStorage(self) -> Path:
        if self.directory == None:
            return app.Storage.get('common_storage').dir()

        _txt = Text.use(self.directory)
        _txt.replaceCwd()

        _dir = Path(_txt.content.text).joinpath('storage')
        _dir.mkdir(exist_ok=True)

        return _dir

    def create_tables(self, items: list) -> None:
        for item in items:
            item.setClsDB(self.db)
            item.setClsTableName(item.table_name)

        self.db.create_tables(items)
