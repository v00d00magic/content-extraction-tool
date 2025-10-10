from typing import List
from Objects.Object import Object
from pathlib import Path
from pydantic import Field, computed_field
from enum import Enum

class PluginWrapperEnum(Enum):
    module = 1
    submodule = 2

    verdict_module = "module"
    verdict_js = "js"

class PluginWrapper(Object):
    path: Path = Field(default=None)
    all_parts: list = []
    category_parts: list = []
    file_name: str = None
    plugin: Object = None

    def constructor(self):
        self.all_parts = self.path.parts

        print(self.all_parts)
        for part in self.all_parts:
            if ".js" in part:
                verdict = PluginWrapperEnum.verdict_js.value
                continue

            if ".py" in part:
                self.file_name = part
            else:
                self.category_parts.append(part)

    @staticmethod
    def scan(dirs: Path) -> List[Object]:
        items: list = []

        # for some reason it goes backwards LOOOL !!!
        for plugin in dirs.rglob('*.py'):
            if plugin.name in ['', '__pycache__', 'Base.py']:
                continue

            items.append(PluginWrapper(path = plugin.relative_to(dirs)))

        return items

    @computed_field
    @property
    def name(self) -> str:
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
