from db.DbConnection import DbConnection
from storage.Storage import Storage
from app.Config import Config
from app.Logger import Logger
from utils.MainUtils import parse_args
from utils.Hookable import Hookable
import asyncio

class App(Hookable):
    events = ["progress"]

    def __init__(self):
        super().__init__()

        self.argv = parse_args()
        self.loop = asyncio.get_event_loop()

    def setup(self):
        from executables.ExecutableMap import ExecutableMap

        self.indexated_scripts = ExecutableMap()

app = App()

config = Config()
env = Config(file_name="env.json",fallback=None)
storage = Storage(config)
logger = Logger(config, storage)

db_connection = DbConnection()
db_connection.attachDb(config, env)
db_connection.createTables()
