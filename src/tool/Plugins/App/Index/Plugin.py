from typing import List, Any
from Objects.Object import Object
from Objects.Section import Section
from pathlib import Path
from pydantic import Field, computed_field
from enum import Enum
import importlib

class PluginEnum(Enum):
    module = 1
    submodule = 2

    verdict_module = "module"
    verdict_js = "js"

class Plugin(Object, Section):
    path: Path = Field(default=None)
    all_parts: list = []
    category_parts: list = []
    stem: str = None
    ext: str = None
    plugin: Any = None

    @property
    def section_name(self) -> list:
        return ["Plugins", "Initialization", "Object"]

    def constructor(self):
        self.all_parts = self.path.parts
        self.stem = self.path.stem
        self.ext = self.path.suffix[1:]

        for part in self.all_parts:
            if f".{self.ext}" in part:
                continue

            self.category_parts.append(part)

        self.log(f"Importing object {self.module_name}")

    @staticmethod
    def scan(dirs: Path) -> List[Object]:
        items: list = []

        for plugin in dirs.rglob('*.py'):
            if plugin.name in ['', '__pycache__', 'Base.py']:
                continue

            # TODO import every class from file
            items.append(Plugin(path = plugin.relative_to(dirs)))

        return items

    @computed_field
    @property
    def module_name(self) -> str:
        parts = self.category_parts.copy()
        parts.append(self.stem)

        return ".".join(parts)

    @computed_field
    @property
    def name(self) -> str:
        parts = self.category_parts.copy()
        parts.append(self.stem)
        parts.append(self.stem)

        return ".".join(parts)

    # bad code practics
    def _imports(self) -> list:
        is_end = self.stem == "__init__"
        title = self.stem
        path: str = f'Plugins.' + self.module_name

        modules = []
        module = importlib.import_module(path)
        assert module != None, f"module {path} not found"

        common_object = getattr(module, title, None)
        assert common_object != None, f"{path} > {title} not found"

        modules.append(common_object)
        self.plugin = common_object

        if hasattr(common_object, "submodules") == True:
            for item in common_object.submodules.all_submodules:
                modules.append(Plugin(plugin=item))

        return modules
