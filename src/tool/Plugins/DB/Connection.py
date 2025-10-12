from Objects.Object import Object
from Objects.Configurable import Configurable

from Objects.classproperty import classproperty
from Plugins.Data.NameDictList import NameDictList
from .ConnectionConfig import ConnectionConfig
from .ConnectionWrapper import ConnectionWrapper
from pydantic import Field

class Connection(Object, Configurable):
    temp_db: ConnectionWrapper = Field()
    db: ConnectionWrapper = Field()
    instance_db: ConnectionWrapper = Field()

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

    @classproperty
    def options(cls) -> NameDictList:
        from Plugins.Arguments.Objects.ObjectArgument import ObjectArgument

        return NameDictList([
            ObjectArgument(
                name = "db.temp.connection",
                object = ConnectionConfig,
                default = ConnectionConfig(
                    protocol = "sqlite",
                    content = ":memory:"
                )
            ),
            ObjectArgument(
                name = "db.content.connection",
                object = ConnectionConfig,
                default = ConnectionConfig(
                    protocol = "sqlite",
                    content = "?cwd?/storage/db/content.db"
                )
            ),
            ObjectArgument(
                name = "db.instance.connection",
                object = ConnectionConfig,
                default = ConnectionConfig(
                    protocol = "sqlite",
                    content = "?cwd?/storage/db/instance.db"
                )
            )
        ])
