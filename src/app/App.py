from db.DbConnection import DbConnection
from storage.Storage import Storage
from app.Config import Config
from app.Logger import Logger
from utils.Hookable import Hookable
import asyncio, sys

class App(Hookable):
    events = ["progress"]

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

    def __init__(self):
        super().__init__()

        self.argv = self._parse_argv()
        self.loop = asyncio.get_event_loop()

    def setup(self):
        from executables.ExecutableMap import ExecutableMap

        self.indexated_scripts = ExecutableMap()

app = App()

config = Config()
env = Config(file_name="env.json",fallback=None)
storage = Storage(config)
logger = Logger(config, storage)

from utils.Web.DownloadManager import DownloadManager

download_manager = DownloadManager(max_concurrent_downloads = 2)

db_connection = DbConnection()
db_connection.attachDb(config, env)
db_connection.createTables()
