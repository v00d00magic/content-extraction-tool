from utils.MainUtils import replace_cwd, replace_src
from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase, DatabaseProxy

class DbConnection:
    def __resolve_str(self, connection_config):
        db = None

        match(connection_config.get("protocol")):
            case "sqlite":
                db = SqliteDatabase(replace_src(replace_cwd(connection_config.get("path"))))

        return db

    def attachDb(self, config, env):
        self.db = self.__resolve_str(config.get("db.content.connection"))
        self.temp_db = SqliteDatabase(":memory:")
        self.instance_db = self.__resolve_str(config.get("db.instance.connection"))

    def __createTablesSection(self, db, models: list):
        proxy = DatabaseProxy()
        for model in models:
            model._meta.table_name = model.table_name
            model.setDbAtClass(proxy)

        proxy.initialize(db)
        db.connect()
        db.create_tables(models, safe=True)

    def createTables(self):
        from db.Models.Content.ContentUnit import ContentUnit
        from db.Models.Relations.ContentUnitRelation import ContentUnitRelation
        from db.Models.Instances.Stat import Stat
        from db.Models.Content.StorageUnit import StorageUnit
        from db.Models.Instances.ServiceInstance import ServiceInstance
        from db.Models.Instances.ArgumentsDump import ArgumentsDump

        self.__createTablesSection(self.temp_db, [ContentUnitRelation, ContentUnit, StorageUnit])
        self.__createTablesSection(self.db, [ContentUnitRelation, ContentUnit, StorageUnit])
        self.__createTablesSection(self.instance_db, [Stat, ServiceInstance, ArgumentsDump])

db_connection = DbConnection()
