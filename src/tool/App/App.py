from Utils.Hookable import Hookable
from Utils.Increment import Increment
from pathlib import Path
import asyncio, sys
import os

class App(Hookable):
    events = ["progress"]

    def __init__(self, context_name = "None"):
        super().__init__()

        self.context = context_name
        self.argv = self._parse_argv()
        self.loop = asyncio.get_event_loop()
        self.executable_index = Increment()
        self.setConsts()

    def _parse_argv(self):
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

    def setAsCommon(self):
        from App import app

        app.setApp(self)

    def setup(self):
        self.setAsCommon()
        self.setupGlobals()
        self.setupMap()

    def setConsts(self):
        self.consts = {}
        self.cwd = Path(os.getcwd())
        self.src = self.cwd.parent

    def setupMap(self):
        from Executables.ExecutableList import ExecutableList

        self.indexated_scripts = ExecutableList()

    def setupGlobals(self):
        from App.Config import Config
        from App.Logger import Logger
        from DB.DbConnection import DbConnection
        from App.Storage import StorageContainer

        self.config = Config(self.cwd.parent)
        self.config.setAsConf()
        self.env = Config(self.cwd.parent, file_name="env.json", fallback=None)

        self.storage = StorageContainer(self.config)
        self.logger = Logger(self.config, self.storage)

        self.db_connection = DbConnection()
        self.db_connection.attachDb(self.config, self.env)
        self.db_connection.createTables()

        from Utils.Web.DownloadManager import DownloadManager

        self.download_manager = DownloadManager(max_concurrent_downloads = 2)
