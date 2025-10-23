from Objects.Object import Object
from Objects.Configurable import Configurable

from Objects.ClassProperty import classproperty
from Plugins.Data.NameDictList import NameDictList
from .ConnectionConfig import ConnectionConfig
from .ConnectionWrapper import ConnectionWrapper
from pydantic import Field

class Connection(Object, Configurable):
    temp_db: ConnectionWrapper = Field()
    db: ConnectionWrapper = Field()
    instance_db: ConnectionWrapper = Field()

    def createTables(self):
        from DB.Models.ContentUnit import ContentUnit
        from DB.Models.ContentUnitRelation import ContentUnitRelation

        self.db.create([ContentUnitRelation, ContentUnit])
        self.temp_db.create([ContentUnitRelation, ContentUnit])
        self.instance_db.create([ContentUnit])

    def getConnectionByName(self, name: str) -> ConnectionWrapper:
        match (name):
            case 'tmp':
                return self.temp_db
            case 'instance':
                return self.instance_db
            case 'content':
                return self.db

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
