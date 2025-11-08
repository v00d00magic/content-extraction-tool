from Objects.Object import Object
from Objects.Section import Section
from Objects.Configurable import Configurable

from Objects.ClassProperty import classproperty
from Plugins.Data.NameDictList import NameDictList
from .ConnectionConfig import ConnectionConfig
from pydantic import Field
from App import app

class Connection(Object, Section, Configurable):
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

            self.log(message = f'Loading DB with id {item.name}')

            item.db = item.connect()
            item.create_tables([ContentUnitRelation, ContentUnit])

        assert len(need_names) > 2, 'one of the dbs is absent: content, tmp, instance'

    @classproperty
    def options(cls) -> NameDictList:
        from Plugins.App.Arguments.Objects.ObjectArgument import ObjectArgument
        from Plugins.App.Arguments.Objects.ListArgument import ListArgument

        return NameDictList([
            ListArgument(
                name = 'db.connections',
                default = [
                    ConnectionConfig(
                        name = 'tmp',
                        protocol = 'sqlite',
                        content = ':memory:'
                    ),
                    ConnectionConfig(
                        name = 'content',
                        protocol = 'sqlite',
                        content = '?cwd?/storage/db/content.db'
                    ),
                    ConnectionConfig(
                        name = 'instance',
                        protocol = 'sqlite',
                        content = '?cwd?/storage/db/instance.db'
                    )
                ],
                orig = ObjectArgument(
                    name = "connection_item",
                    object = ConnectionConfig
                )
            )
        ])
