from Plugins.App.Logger.LogParts.LogKind import LogKind
from Plugins.Data.NameDictList import NameDictList
from .Plugin import Plugin
from Objects.Section import Section
from Objects.Object import Object
from pathlib import Path
from App import app

class PluginsCounter():
    total = 0
    success = 0
    submodules = 0
    errors = 0

class PluginsList(Object, Section):
    items: NameDictList = []

    def constructor(self):
        self.items = NameDictList(items = [])

    @property
    def section_name(self) -> list:
        return ["Plugins", "Initialization"]

    def load(self):
        self.log("Loading plugins list: ")

        counters = PluginsCounter()
        search_dir: Path = app.cwd.joinpath("Plugins")

        for item in Plugin.scan(search_dir): # iterating
            module = None
            counters.total += 1

            try:
                plugins = item._imports()

                for plugin in plugins:
                    self.items.append(plugin)
            except AssertionError as e:
                self.log_error(f"AssertionError when importing {item.name}: {str(e)}, probaly not an executable")
            except Exception as e:
                raise e
                counters.errors += 1
                self.log_error(e, exception_prefix=f"Did not imported module {item.name}: ")

        counters.success = len(self.items.items)

        self.log(f"Found total {counters.total} objects, {counters.success} successfully, {counters.submodules} submodules, {counters.errors} errors")

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
