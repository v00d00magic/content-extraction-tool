from Objects.Configurable import Configurable
from DB.DBWrapper import DBWrapper

class DbConnection(Configurable):
    def __init__(self):
        self.updateConfig()

    def attachDbs(self, config, env):
        self.temp_db = DBWrapper("temp", DBWrapper.getByConfig({
            "protocol": "sqlite",
            "path": ":memory:"
        }))
        self.db = DBWrapper("content", DBWrapper.getByConfig(config.get("db.content.connection")))
        self.instance_db = DBWrapper("instance", DBWrapper.getByConfig(config.get("db.instance.connection")))

    def createTables(self):
        from DB.Models.Content.ContentUnit import ContentUnit
        from DB.Links.ContentUnitRelation import ContentUnitRelation
        from DB.Models.Instances.Stat import Stat
        from DB.Models.Content.StorageUnit import StorageUnit
        from DB.Models.Instances.ServiceInstance import ServiceInstance
        from DB.Models.Instances.ArgumentsDump import ArgumentsDump

        self.db.create([ContentUnitRelation, ContentUnit, StorageUnit])
        self.temp_db.create([ContentUnitRelation, ContentUnit, StorageUnit])
        self.instance_db.create([Stat, ServiceInstance, ArgumentsDump])

    @classmethod
    def declareSettings(cls):
        from Declarable.Arguments import ObjectArgument

        items = {}
        items["db.content.connection"] = ObjectArgument({
            "default": {
                "protocol": "sqlite",
                "path": "?cwd?/storage/db/content.db"
            }
        })
        items["db.instance.connection"] = ObjectArgument({
            "default": {
                "protocol": "sqlite",
                "path": "?cwd?/storage/db/instance.db"
            }
        })
        return items
