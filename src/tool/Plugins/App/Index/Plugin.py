from typing import List, Any
from Objects.Object import Object
from pathlib import Path
from pydantic import Field, computed_field
from enum import Enum
import importlib

class PluginEnum(Enum):
    module = 1
    submodule = 2

    verdict_module = "module"
    verdict_js = "js"

class Plugin(Object):
    module: Any = Field(default=None)

    @property
    def name(self) -> str:
        parts = self.module.meta.class_module.split('.')
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

    # TODO refactor
    def tryToImportFromModuleName(self, title: str, parts: List[str]):
        prefix = 'Plugins.'
        module_name = ".".join(parts + [title])

        module = importlib.import_module(prefix + module_name)
        assert module != None, f"module {module_name} not found"

        common_object = getattr(module, title, None)
        assert common_object != None, f"{module_name} > {title} not found"
        assert hasattr(common_object, 'meta'), f"{module_name} does not extends Object"

        if hasattr(common_object, 'mount'):
            common_object.mount()

        return common_object

    def importSubmodules(self) -> List[Object]:
        payload_plugins = []

        for submodule in self.module.submodules.all_submodules:
            payload_plugins.append(Plugin(module = submodule))

        return payload_plugins
