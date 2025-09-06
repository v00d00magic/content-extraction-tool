from pathlib import Path
from resources.Consts import consts
from app.App import logger
import importlib
import time

class ExecutableMap:
    items = {}
    RESULT_MODULE = 1
    RESULT_SUBMODULE = 2

    def __init__(self):
        logger.log("Getting executables list...", section="ExecutableMap!Initialization")

        total = 0
        successes = 0
        successes_submodules = 0
        errors = 0

        _lists = self.get_list()
        for item in _lists:
            module = None
            parts = None
            total += 1

            try:
                start_time = time.time()

                parts = self.split(item)
                module = self.do_import(parts)

                end_time = time.time()

                logger.log(f"Imported module {module.full_name()} in {round(end_time - start_time, 2)}s", section="ExecutableMap!Initialization")

                _item = self.register(module)

                successes +=1

                if _item == ExecutableMap.RESULT_SUBMODULE:
                    successes_submodules += 1
            except AssertionError as e:
                logger.log(f"AssertionError when importing {".".join(parts.get("parts"))}: {str(e) }, probaly not an executable", section="ExecutableMap!Initialization")
            except Exception as e:
                errors += 1
                logger.log(e, section="ExecutableMap!Initialization", prefix=f"Did not imported module: ")

        logger.log(f"Found total {total} scripts, {successes} successfully, {successes_submodules} submodules, {errors} errors", section="ExecutableMap!Initialization")

    def split(self, path):
        parts = str(path).split("\\")
        submodule = None
        name = ""

        common_parts = []
        name_parts = []

        # Splitting
        for part in parts:
            # end of the path
            if ".py" in part:
                name = part
                continue

            # we got to the additional modules
            if part in ["Receivations", "Acts", "Extractors", "ExternalExtractors"]:
                submodule = part
            else:
                common_parts.append(part)

            name_parts.append(part)

        return {
            "parts": name_parts,
            "name": name,
            "common": common_parts,
            "submodule": submodule,
        }

    def do_import(self, data):
        is_end = data.get("name") == "__init__.py"
        title = "Method"
        module_path = f'executables.list.' + ".".join(data.get("parts"))
        if is_end == True:
            title = "Implementation"
        else:
            module_path += "." + data.get("name")[:-3]

        module = importlib.import_module(module_path)
        assert module != None, f"module {module_path} not found"

        common_object = getattr(module, title, None)
        assert common_object != None, f"{module_path} > {title} not found"

        return common_object

    def register(self, module):
        main_module = module.main_module

        if main_module == None:
            self.items[module.full_name()] = module

            return ExecutableMap.RESULT_MODULE
        else:
            logger.log(f"Imported module {module.full_name()} to {main_module.full_name()}", section="ExecutableMap!Initialization")

            self.items[main_module.full_name()].add_submodule(module)
            self.items[module.full_name()] = module

            return ExecutableMap.RESULT_SUBMODULE

    def get_list(self):
        list = []

        executables_dir = consts.get('executables')
        executables_list_dir = Path(f"{executables_dir}\\list")

        for script in executables_list_dir.rglob('*.py'):
            path = script.relative_to(executables_list_dir)
            if script.name in ['', '__pycache__', 'Base.py']:
                continue

            list.append(path)

        return list

    def items_by_class(self, class_name = None):
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
