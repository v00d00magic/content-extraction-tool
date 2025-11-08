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
    module: Any = None

    @property
    def section_name(self) -> list:
        return ["Plugins", "Initialization", "Object"]

    @property
    def name(self) -> str:
        parts = self.module.class_module.split('.')
        class_name = self.module.class_name

        return '.'.join(parts[1:] + [class_name])

    @staticmethod
    def fromPath(path: Path):
        title = path.stem
        ext = path.suffix[1:]
        all_parts = path.parts
        category_parts: list = []
        for part in all_parts:
            if f".{ext}" in part:
                continue

            category_parts.append(part)

        plugin = Plugin()
        plugin.module = plugin.tryToImportFromModuleName(title, category_parts)

        return plugin

    def tryToImportFromModuleName(self, title: str, parts: list[str]):
        prefix = 'Plugins.'
        module_name = ".".join(parts + [title])

        module = importlib.import_module(prefix + module_name)
        assert module != None, f"module {module_name} not found"

        common_object = getattr(module, title, None)
        assert common_object != None, f"{module_name} > {title} not found"

        # calling object class_name and checking if this an object
        self.log(f"Loaded object {common_object.class_name}")

        return common_object
