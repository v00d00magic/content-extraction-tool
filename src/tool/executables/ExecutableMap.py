from pathlib import Path
from app.App import app, logger
import importlib
import time

class ExecutableMap:
    section_name = ["Executables", "Initialization"]

    items = {}
    js_modules = {}

    RESULT_MODULE = 1
    RESULT_SUBMODULE = 2

    def __init__(self):
        self.putItems()

    def putItems(self):
        logger.log("Getting executables list...", section=self.section_name)

        counters = {
            "total": 0,
            "success": 0,
            "submodules": 0,
            "errors": 0
        }
        executables_dir = app.cwd.joinpath("executables")

        # for some reason it goes backwards LOOOL
        for item in self.scanDirectory(executables_dir.joinpath("list")): # iterating
            start_time = time.time()

            module = None
            parts = None
            counters["total"] += 1

            try:
                parts = self.parseFile(item)
                match(parts.get("verdict")):
                    case "module":
                        module = self.doImport(parts)
                        end_time = time.time()

                        logger.log(f"Imported module {module.getName()} in {round(end_time - start_time, 3)}s", section=self.section_name)

                        _item = self.register(module)

                        counters["success"] +=1
                        if _item == ExecutableMap.RESULT_SUBMODULE:
                            counters["submodules"] += 1
                    case "js":
                        self.js_modules[".".join(parts.get("parts"))] = parts.get("name")

            except AssertionError as e:
                logger.log(f"AssertionError when importing {".".join(parts.get("parts"))}: {str(e) }, probaly not an executable", section=self.section_name)
            except Exception as e:
                counters["errors"] += 1
                logger.log(e, section=self.section_name, prefix=f"Did not imported module {".".join(parts.get("parts"))}: ")

        logger.log(f"Found total {counters["total"]} scripts, {counters["success"]} successfully, {counters["submodules"]} submodules, {counters["errors"]} errors", section=self.section_name)

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

    def parseFile(self, path):
        parts = str(path).split("\\")
        name = ""

        verdict = "module"
        common_parts = []
        name_parts = []

        for part in parts:
            if ".js" in part:
                verdict = "js"
                continue
            if ".py" in part:
                name = part
                continue

            common_parts.append(part)
            name_parts.append(part)

        return {
            "verdict": verdict,
            "parts": name_parts,
            "name": name,
        }

    def doImport(self, data):
        is_end = data.get("name") == "__init__.py"
        title = "Implementation"
        module_path = f'executables.list.' + ".".join(data.get("parts"))
        if is_end == False:
            module_path += "." + data.get("name")[:-3]

        module = importlib.import_module(module_path)
        assert module != None, f"module {module_path} not found"

        common_object = getattr(module, title, None)
        assert common_object != None, f"{module_path} > {title} not found"

        if hasattr(module, "locale_keys") == True:
            common_object.loadKeys(getattr(module, "locale_keys"))

        common_object.docs = common_object.defineMeta()

        return common_object

    def register(self, module):
        main_module = module.main_module

        if main_module == None:
            self.items[module.getName()] = module # adding to common list

            '''
            for inh_module in module.getInheritFrom():
                for inh_sub_module in inh_module.submodules:
                    self.items.get(module.getName()).submodules.append(inh_sub_module)
            '''
            return ExecutableMap.RESULT_MODULE
        else:
            logger.log(f"Injected module {module.getName()} to {main_module.getName()}", section=self.section_name)

            self.items[main_module.getName()].addSubmodule(module) # registering to main module
            self.items[module.getName()] = module

            return ExecutableMap.RESULT_SUBMODULE
