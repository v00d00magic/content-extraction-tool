from Objects.Object import Object

from Objects.ClassProperty import classproperty
from Plugins.Data.NameDictList import NameDictList
from .ConnectionItem import ConnectionItem
from pydantic import Field
from App import app

class Connection(Object):
    '''
    Wrapper of the peewee databases
    '''

    dbs: NameDictList = []

    def constructor(self):
        from DB.Models.ContentUnit import ContentUnit
        from DB.Models.ContentUnitRelation import ContentUnitRelation

        need_names = []

        for item in self.dbs.toList():
            if item.name in ['content', 'tmp', 'instance']:
                need_names.append(item.name)

            self.log(f'Loading DB with id {item.name}')

            item.db = item.connect()
            item.create_tables([ContentUnitRelation, ContentUnit])

        assert len(need_names) > 2, 'one of the dbs is absent: content, tmp, instance'

    @staticmethod
    def mount():
        from App import app

        app.Config.updateCompare()
        connection = Connection(dbs = NameDictList(app.Config.get('db.connections')))

        app.mount('DbConnection', connection)

    @classproperty
    def options(cls) -> NameDictList:
        from Plugins.App.Arguments.Objects.ObjectArgument import ObjectArgument
        from Plugins.App.Arguments.Objects.ListArgument import ListArgument

        return NameDictList([
            ListArgument(
                name = 'db.connections',
                default = [
                    ConnectionItem(
                        name = 'tmp',
                        protocol = 'sqlite',
                        data = ':memory:'
                    ),
                    ConnectionItem(
                        name = 'content',
                        protocol = 'sqlite',
                    ),
                    ConnectionItem(
                        name = 'instance',
                        protocol = 'sqlite',
                    )
                ],
                orig = ObjectArgument(
                    name = "connection_item",
                    object = ConnectionItem
                )
            )
        ])
