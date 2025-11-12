from Plugins.App.Storage.StorageItem import StorageItem
from Objects.Configurable import Configurable
from Plugins.Data.NameDictList import NameDictList
from Objects.Object import Object
from Objects.ClassProperty import classproperty
from pydantic import Field
from pathlib import Path

class Storage(Object, Configurable):
    items: dict = Field(default={})
    common: Path = Field(default=None)

    def register(self):
        for name in ['config', 'dbs', 'exports', 'common_storage', 'tmp_exports', 'logs', 'bin']:
            self.items[name] = StorageItem(
                root = self.common, 
                dir_name = name
            )

    def get(self, name):
        return self.items.get(name)

    @staticmethod
    def mount():
        from App import app
        from Plugins.Data.Text import Text

        storage = Storage()
        text = Text.use(
            text = app.Config.get('storage.path')
        )
        text.replaceCwd()

        storage.common = Path(text.content.text)
        storage.register()

        app.mount('Storage', storage)

    @classproperty
    def options(cls) -> NameDictList:
        from Plugins.App.Arguments.Types.StringArgument import StringArgument

        return NameDictList([
            StringArgument(
                name = "storage.path",
                default = "?cwd?/storage",
            )
        ])
