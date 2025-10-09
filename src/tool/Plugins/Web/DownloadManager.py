
from Plugins.App.Logger.LogParts.LogKind import LogKind
from Objects.Hookable import Hookable
from App import app
from pathlib import Path
import asyncio, aiohttp, os, time
from Objects.Configurable import Configurable
from Objects.Increment import Increment

class DownloadManagerItem():
    section_name = ["DownloadManager", "Item"]

    def __init__(self, url: str, dir: str):
        self.url = url
        self.dir = dir
        self.pause_flag = asyncio.Event()
        self.task = None
        self.stat = {
            "downloaded": 0,
            "size": 0,
            "start_time": 0,
            "percentage": 0
        }
        self.status = "end"
        self.id = 0

    def getPrefix(self):
        return f"DownloadItem->{self.id}"

    async def startDownload(self, manager = None):
        self.manager = manager

        async with self.manager._session as session:
            self.task = await asyncio.create_task(self.download(session))

            return self.task

    async def download(self, session):
        DOWNLOAD_URL = self.url
        DOWNLOAD_DIR = self.dir

        app.logger.log(f"Downloading {DOWNLOAD_URL}", section=self.section_name, id_prefix = self.getPrefix())

        async with self.manager.semaphore:
            async with session.get(DOWNLOAD_URL, allow_redirects=True, headers=self.manager._headers) as response:
                STATUS = response.status

                if STATUS == 404 or STATUS == 403:
                    raise FileNotFoundError('File not found')

                if DOWNLOAD_DIR != None and Path(DOWNLOAD_DIR).is_file():
                    app.logger.log(f"{DOWNLOAD_URL} is already downloaded", section = self.section_name, id_prefix = self.getPrefix())

                    return response

                CONTENT_LENGTH = response.headers.get("Content-Length", 0)
                self.stat["downloaded"] = 0
                self.stat["size"] = int(CONTENT_LENGTH)
                self.stat["start_time"] = time.time()
                if DOWNLOAD_DIR != None:
                    with open(DOWNLOAD_DIR, 'wb') as f:
                        async for chunk in response.content.iter_chunked(1024):
                            #await self["pause_flag"].wait() FIXME
                            f.write(chunk)

                            elapsed_time = time.time() - self.stat.get("start_time")
                            expected_time = len(chunk)
                            self.stat["downloaded"] += expected_time
                            if self.stat.get("size", 0) != 0:
                                self.stat["percentage"] = (self.stat.get("downloaded") / self.stat.get("size")) * 100

                            self.status = "downloading"
                            self.manager.trigger("downloading", self)

                            if self.manager.speed_limit_kbps:
                                expected_time = expected_time / (self.speed_limit_bytes)
                                if expected_time > elapsed_time:
                                    await asyncio.sleep(expected_time - elapsed_time)

                    self.status = "success"
                    self.manager.trigger("success", self)

                    app.logger.log(f"Downloading complete", section=self.section_name, kind=LogKind.KIND_SUCCESS, id_prefix = self.getPrefix())

                return response

# FIXME: rewrite
class DownloadManager(Hookable, Configurable):
    section_name = "DownloadManager"

    @classmethod
    def declareSettings(cls):
        from Declarable.Documentation import global_documentation
        from Declarable.Arguments import IntArgument, StringArgument

        global_documentation.loadKeys({
            "net.max_speed.name": {
                "en_US": "Max speed",
            },
            "net.useragent.name": {
                "en_US": "User-Agent",
            },
            "net.max_speed.definition": {
                "en_US": "Max speed for web operations (in Kbps)",
            },
            "net.timeout.name": {
                "en_US": "Timeout",
            },
            "net.timeout.definition": {
                "en_US": "Timeout for web operations",
            }
        })

        items = {}
        items["net.max_speed"] = IntArgument({
            "default": 2000, # kbs
            "docs": {
                "name": global_documentation.get("net.max_speed.name"),
                "definition": global_documentation.get("net.max_speed.definition"),
            },
        })
        items["net.useragent"] = StringArgument({
            "default": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
            "docs": {
                "name": global_documentation.get("net.useragent.name"),
            },
        })
        items["net.timeout"] = IntArgument({
            "default": 100,
            "docs": {
                "name": global_documentation.get("net.timeout.name"),
                "definition": global_documentation.get("net.timeout.definition"),
            },
        })

        return items

    def __init__(self, max_concurrent_downloads: int = 3, speed_limit_kbps: int = app.config.get("net.max_speed")):
        super().__init__()

        self.updateConfig()
        self.queue = []
        self.max_concurrent_downloads = max_concurrent_downloads
        self.speed_limit_kbps = speed_limit_kbps
        self.semaphore = asyncio.Semaphore(self.max_concurrent_downloads)
        self._timeout = app.config.get("net.timeout")
        self.download_index = Increment()
        self._headers = {
            "User-Agent": app.config.get("net.useragent")
        }

    def _check_session(self):
        if getattr(self, "_session", None) == None:
            timeout = aiohttp.ClientTimeout(total=self._timeout)
            self._session = aiohttp.ClientSession(timeout = timeout)

    def _selfDownloadHook(self, d):
        print(d.get("status"))
        print(d.get("percentage"))

    async def addDownload(self, download_item):
        download_item.id = self.download_index.getIndex()
        self._check_session()
        self.queue.append(download_item)

        return await download_item.startDownload(self)

    def _findDownloadByURL(self, url):
        for item in self.queue:
            if item.get("url") == url:
                return item

        return None

    def pause(self, url):
        item = self._findDownloadByURL(url)
        if item == None:
            return None

        item["pause_flag"].clear()

    def resume(self, url):
        item = self._findDownloadByURL(url)
        if item == None:
            return None

        item["pause_flag"].set()

    def set_max_concurrent_downloads(self, value):
        self.max_concurrent_downloads = int(value)
        self.semaphore = asyncio.Semaphore(self.max_concurrent_downloads)

    def set_speed_limit_kbps(self, value):
        self.speed_limit_kbps = int(value)

    @property
    def speed_limit_bytes(self):
        return self.speed_limit_kbps * 1024
