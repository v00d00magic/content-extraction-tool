from Objects.Object import Object
from Objects.Increment import Increment
from Objects.Hookable import Hookable
from Objects.Section import Section
from Plugins.Data.NameDictList import NameDictList
from pathlib import Path
from typing import Any
import asyncio, sys
import os

from pydantic import Field

class App(Object):
    context_name: str = Field(default = 'none')
    settings: dict = {}
    cwd: str = None
    src: str = None
    loop: Any = None
    ExecutablesTable: Any = None

    # TODO remove these fields
    Config: Any = None
    Env: Any = None
    Storage: Any = None
    Logger: Any = None
    Storage: Any = None
    DbConnection: Any = None
    DownloadManager: Any = None
    argv: dict = None

    class HooksManager(Hookable.HooksManager):
        @property
        def events(self) -> list:
            return ["progress"]

    class _ExecutablesTable(Section):
        def __init__(self):
            from .Index.PluginsList import PluginsList

            self.executable_index = Increment()
            self.list = PluginsList()
            self.list.load()
            self.calls = []

    def loadPlugins(self):
        self.ExecutablesTable = self._ExecutablesTable()

    def _constructor(self):
        self.argv = self._parse_argv()
        self.cwd = Path(os.getcwd())
        self.src = self.cwd.parent
        self.loop = asyncio.get_event_loop()

    def _parse_argv(self):
        # didn't changed since sep.2024
        args = sys.argv
        parsed_args = {}
        key = None
        for arg in args[1:]:
            if arg.startswith('--'):
                if key:
                    parsed_args[key] = True
                key = arg[2:]
                parsed_args[key] = True
            else:
                if key:
                    parsed_args[key] = arg
                    key = None
                else:
                    pass

        return parsed_args
