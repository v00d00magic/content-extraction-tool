from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase, DatabaseProxy
from Utils.Data.Text import Text
from playhouse.shortcuts import ThreadSafeDatabaseMetadata

class DBWrapper:
    def __init__(self, name, db):
        self.db_name = name
        self.db_ref = db

    @classmethod
    def getByConfig(cls, connection_config):
        db = None

        match(connection_config.get("protocol")):
            case "sqlite":
                db = SqliteDatabase(Text(connection_config.get("path")).cwdReplacement().get())

        return db

    def create(self, models: list):
        proxy = DatabaseProxy()
        for model in models:
            model._meta.table_name = model.table_name
            model._meta.model_metadata_class = ThreadSafeDatabaseMetadata
            model.setWrapperToModel(self)
            model.bind(proxy)

        proxy.initialize(self.db_ref)
        self.db_ref.connect()
        self.db_ref.create_tables(models, safe=True)
