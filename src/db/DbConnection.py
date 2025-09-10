from utils.MainUtils import replace_cwd, replace_src
from peewee import SqliteDatabase, MySQLDatabase, PostgresqlDatabase, DatabaseProxy

database_proxy = DatabaseProxy()

class DbConnection:
    conf = {}

    def __resolve_str(self, i_str):
        conn_list = i_str.split(":///", 1)
        conn_type = conn_list[0]
        db = None

        match(conn_type):
            case "sqlite":
                if conn_list[1] == ":memory:":
                    db = SqliteDatabase(":memory:")
                else:
                    connection_path = replace_src(replace_cwd(conn_list[1]))
                    db = SqliteDatabase(connection_path)

        return db

    def attachDb(self, config, env):
        self.db = self.__resolve_str(config.get("db.content.connection"))
        self.instance_db = self.__resolve_str(config.get("db.instance.connection"))

    def __createTablesSection(self, db, models: list):
        proxy = DatabaseProxy()
        for model in models:
            model._meta.table_name = model.table_name
            model._meta.database = proxy

        proxy.initialize(db)
        db.connect()
        db.create_tables(models, safe=True)

    def createTables(self):
        from db.Models.Content.ContentUnit import ContentUnit
        from db.Models.Relations.ContentUnitRelation import ContentUnitRelation
        from db.Models.Instances.Stat import Stat
        from db.Models.Content.StorageUnit import StorageUnit
        from db.Models.Instances.ServiceInstance import ServiceInstance

        self.__createTablesSection(self.db, [ContentUnitRelation, ContentUnit, StorageUnit])
        self.__createTablesSection(self.instance_db, [Stat, ServiceInstance])

db_connection = DbConnection()
