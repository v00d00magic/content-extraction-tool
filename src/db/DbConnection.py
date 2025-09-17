from utils.Data.Text import Text
from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase, DatabaseProxy

class DbConnection:
    @classmethod
    def getByConfig(cls, connection_config):
        db = None

        match(connection_config.get("protocol")):
            case "sqlite":
                db = SqliteDatabase(Text(connection_config.get("path")).cwdReplacement().srcReplacement().get())

        return db

    @classmethod
    def create(cls, db, models: list):
        proxy = DatabaseProxy()
        for model in models:
            model._meta.table_name = model.table_name
            model.setDbAtClass(proxy)

        proxy.initialize(db)
        db.connect()
        db.create_tables(models, safe=True)

    def attachDb(self, config, env):
        self.db = DbConnection.getByConfig(config.get("db.content.connection"))
        self.temp_db = SqliteDatabase(":memory:")
        self.instance_db = DbConnection.getByConfig(config.get("db.instance.connection"))

    def createTables(self):
        from db.Models.Content.ContentUnit import ContentUnit
        from db.Models.Relations.ContentUnitRelation import ContentUnitRelation
        from db.Models.Instances.Stat import Stat
        from db.Models.Content.StorageUnit import StorageUnit
        from db.Models.Instances.ServiceInstance import ServiceInstance
        from db.Models.Instances.ArgumentsDump import ArgumentsDump

        DbConnection.create(self.temp_db, [ContentUnitRelation, ContentUnit, StorageUnit])
        DbConnection.create(self.db, [ContentUnitRelation, ContentUnit, StorageUnit])
        DbConnection.create(self.instance_db, [Stat, ServiceInstance, ArgumentsDump])

db_connection = DbConnection()
