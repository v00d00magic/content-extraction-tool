from Plugins.App.Logger.LogParts.LogKind import LogKind
from .PluginWrapper import PluginWrapper
from Objects.Section import Section
from Objects.Object import Object
from pathlib import Path
from App import app
import importlib
import time

class PluginsCounter():
    total = 0
    success = 0
    submodules = 0
    errors = 0

class PluginsList(Object, Section):
    items: dict = {}

    @property
    def section_name(self) -> list:
        return ["Executables", "Initialization"]

    def load(self):
        self.log("Creating executables list...")

        counters = PluginsCounter()
        search_dir: Path = app.cwd.joinpath("Plugins")
        plguins = PluginWrapper.scan(search_dir)

        for item in plguins: # iterating
            module = None
            result = PluginWrapper.partsToResult(item)
            counters["total"] += 1

            try:
                match(result.verdict):
                    case ExecutableListResult.VERDICT_MODULE:
                        module = result.doImport()

                        app.logger.log(f"Imported module {module.getName()}", section=self.section_name)
                        counters["success"] +=1

                        match(ExecutableListResult.getType(module)):
                            case ExecutableListResult.MODULE:
                                self.items[module.getName()] = module
                            case ExecutableListResult.SUBMODULE:
                                app.logger.log(f"Injected module {module.getName()} into {module.main_module.getName()} as submodule", section=self.section_name)

                                self.items[module.getName()] = module
                                self.items[module.main_module.getName()].addSubmodule(module)

                                counters["submodules"] += 1
                    case ExecutableListResult.VERDICT_JS:
                        pass

            except AssertionError as e:
                app.logger.log(f"AssertionError when importing {result.getName()}: {str(e) }, probaly not an executable", section=self.section_name, kind = LogKind.KIND_ERROR)
            except Exception as e:
                counters["errors"] += 1
                app.logger.log(e, section=self.section_name, prefix=f"Did not imported module {result.getName()}: ", kind = LogKind.KIND_ERROR)

        app.logger.log(f"Found total {counters["total"]} scripts, {counters["success"]} successfully, {counters["submodules"]} submodules, {counters["errors"]} errors", section=self.section_name)

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
