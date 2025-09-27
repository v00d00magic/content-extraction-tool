from Utils.Wrap import Wrap
from pathlib import Path
from App import app
import importlib
import time

class ExecutableListResult(Wrap):
    verdict: str = None
    parts: list = None
    name: str = None

    MODULE = 1
    SUBMODULE = 2

    VERDICT_MODULE = "module"
    VERDICT_JS = "js"

    def getName(self):
        return ".".join(self.parts)

    def doImport(self):
        is_end = self.name == "__init__.py"
        title = "Implementation"
        module_path = f'Executables.list.' + self.getName()
        if is_end == False:
            module_path += "." + self.name[:-3]

        module = importlib.import_module(module_path)
        assert module != None, f"module {module_path} not found"

        common_object = getattr(module, title, None)
        assert common_object != None, f"{module_path} > {title} not found"

        if hasattr(module, "locale_keys") == True:
            common_object.loadKeys(getattr(module, "locale_keys"))

        common_object.docs = common_object.defineMeta()

        return common_object

    @staticmethod
    def getType(module):
        main_module = module.main_module

        if main_module == None:
            return ExecutableListResult.MODULE
        else:
            return ExecutableListResult.SUBMODULE

    @staticmethod
    def partsToResult(path):
        parts = Path(path).parts
        name = ""

        verdict = ExecutableListResult.VERDICT_MODULE
        common_parts = []
        name_parts = []

        for part in parts:
            if ".js" in part:
                verdict = ExecutableListResult.VERDICT_JS
                continue
            if ".py" in part:
                name = part
                continue

            common_parts.append(part)
            name_parts.append(part)

        return ExecutableListResult({
            "verdict": verdict,
            "parts": name_parts,
            "name": name,
        })

class ExecutableList:
    section_name = ["Executables", "Initialization"]
    items = {}

    def __init__(self):
        self.putItems()

    def putItems(self):
        app.logger.log("Getting executables list...", section=self.section_name)

        counters = {
            "total": 0,
            "success": 0,
            "submodules": 0,
            "errors": 0
        }

        executables_dir = app.cwd.joinpath("Executables")

        # for some reason it goes backwards LOOOL
        for item in self.scanDirectory(executables_dir.joinpath("list")): # iterating
            module = None
            result = ExecutableListResult.partsToResult(item)
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
                app.logger.log(f"AssertionError when importing {result.getName()}: {str(e) }, probaly not an executable", section=self.section_name)
            except Exception as e:
                counters["errors"] += 1
                app.logger.log(e, section=self.section_name, prefix=f"Did not imported module {result.getName()}: ")

        app.logger.log(f"Found total {counters["total"]} scripts, {counters["success"]} successfully, {counters["submodules"]} submodules, {counters["errors"]} errors", section=self.section_name)

    def scanDirectory(self, executables_dir):
        list = []

        for script in executables_dir.rglob('*.py'):
            path = script.relative_to(executables_dir)
            if script.name in ['', '__pycache__', 'Base.py']:
                continue

            list.append(path)

        return list

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
