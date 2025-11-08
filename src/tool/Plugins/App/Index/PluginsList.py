from Plugins.App.Logger.LogParts.LogKind import LogKind
from Plugins.Data.NameDictList import NameDictList
from .Plugin import Plugin
from Objects.Section import Section
from typing import List
from Objects.Object import Object
from pathlib import Path
from App import app

class PluginsList(Object, Section):
    items: NameDictList = []

    def constructor(self):
        self.items = NameDictList(items = [])

    @property
    def section_name(self) -> list:
        return ["Plugins", "Initialization"]

    def load(self):
        self.log("Loading plugins list: ")

        counters = [0, 0, 0, 0]
        search_dir: Path = app.cwd.joinpath("Plugins")

        for item_path in PluginsList.scan(search_dir): # iterating
            counters[0] += 1

            try:
                plugin = Plugin.fromPath(path = item_path)
                self.items.append(plugin)
            except AssertionError as e:
                self.log_error(f"AssertionError when importing {item_path.name}: {str(e)}, probaly not an executable")
            except Exception as e:
                counters[2] += 1
                self.log_error(e, exception_prefix=f"Did not imported module {item_path.name}: ")
                #raise e

        counters[1] = len(self.items.items)

        self.log(f"Found total {counters[0]} objects, {counters[1]} successfully, {counters[0]} submodules, {counters[3]} errors")

    @staticmethod
    def scan(dirs: Path) -> List[Path]:
        items: list = []

        for plugin in dirs.rglob('*.py'):
            if plugin.name in ['', '__pycache__', 'Base.py']:
                continue

            yield plugin.relative_to(dirs)

    def listByClass(self, class_name = None):
        output = []
        for item_name, item in self.items.items():
            if class_name != None:
                if class_name != item.self_name:
                    continue

            output.append(item)

        return output

    def find(self, key, class_name = None):
        _item = self.items.get(key)

        if class_name != None:
            if class_name != _item.self_name:
                return None

        return _item
