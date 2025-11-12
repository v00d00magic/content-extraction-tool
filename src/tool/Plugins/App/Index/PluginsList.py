from Plugins.App.Logger.LogParts.LogKind import LogKind
from Plugins.Data.NameDictList import NameDictList
from .Plugin import Plugin
from typing import List
from Objects.Object import Object
from pathlib import Path
from App import app

class PluginsList(Object):
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
            counters[3] += 1

            try:
                plugin = Plugin.fromPath(path = item_path)
                # calling object class_name and checking if this an object
                self.log(f"Loaded object {plugin.module.meta.class_name_str}")
                self.items.append(plugin)

                for subplugin in plugin.importSubmodules():
                    counters[2] += 1

                    self.log(f"Loaded object {subplugin.module.meta.class_name_str}")
                    self.items.append(subplugin)

                counters[3] -= 1
            except AssertionError as e:
                self.log_error(f"AssertionError when importing {item_path.name}: {str(e)}, probaly not an executable")
            except AttributeError as e:
                self.log_error(e, exception_prefix=f"Did not imported module {item_path.name}: ")
                raise e
            except Exception as e:
                raise e

        counters[1] = len(self.items.items)

        self.log(f"Found total {counters[0]} objects, {counters[1]} successfully, {counters[2]} submodules, {counters[3]} errors")

    @staticmethod
    def scan(dirs: Path) -> List[Path]:
        items: list = []
        files = dirs.rglob('*.py')
        files = list(files)
        priority: list = ['App\Config\Config.py', 'App\Logger\Logger.py', 'App\Env\Env.py', 'App\Storage\Storage.py', 'App\DbConnection\DbConnection.py', 'Web\DownloadManager\DownloadManager']
        n = len(files)
        current_path = app.cwd.joinpath("Plugins")

        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                _name = files[j].relative_to(current_path)
                if _name in priority and priority.index(_name) < priority.index(files[min_idx]):
                    min_idx = j
            files[i], files[min_idx] = files[min_idx], files[i]

        for plugin in files:
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
