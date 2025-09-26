from app.App import app
from app.Config import Config
from app.Logger import Logger
from db.DbConnection import DbConnection
from app.Storage import StorageContainer

config = Config(app.cwd.parent)
config.setAsConf()
env = Config(app.cwd.parent, file_name="env.json", fallback=None)

storage = StorageContainer(config)
logger = Logger(config, storage)

db_connection = DbConnection()
db_connection.attachDb(config, env)
db_connection.createTables()

from utils.Web.DownloadManager import DownloadManager

download_manager = DownloadManager(max_concurrent_downloads = 2)
