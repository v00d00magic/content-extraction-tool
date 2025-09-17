from app.App import logger
from utils.Hookable import Hookable
from app.App import config
from pathlib import Path
import asyncio, aiohttp, os, time

class DownloadManagerItem():
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

# FIXME: rewrite
class DownloadManager(Hookable):
    def __init__(self, max_concurrent_downloads: int = 3, speed_limit_kbps: int = config.get("net.max_speed")):
        super().__init__()
        
        self.queue = []
        self.max_concurrent_downloads = max_concurrent_downloads
        self.speed_limit_kbps = speed_limit_kbps
        self.semaphore = asyncio.Semaphore(self.max_concurrent_downloads)
        self._timeout = config.get("net.timeout")
        self._headers = {
            "User-Agent": config.get("net.useragent")
        }

    def _check_session(self):
        if getattr(self, "_session", None) == None:
            timeout = aiohttp.ClientTimeout(total=self._timeout)
            self._session = aiohttp.ClientSession(timeout = timeout)

    def _selfDownloadHook(self, d):
        print(d.get("status"))
        print(d.get("percentage"))

    async def addDownload(self, download_item):
        self._check_session()
        self.queue.append(download_item)

        return await self.startDownload(self.queue[-1])

    async def startDownload(self, queue_element: DownloadManagerItem):
        async with self._session as session:
            queue_element.task = await asyncio.create_task(self.download(session, queue_element))

            return queue_element.task

    async def download(self, session, queue_element):
        DOWNLOAD_URL = queue_element.url
        DOWNLOAD_DIR = queue_element.dir

        logger.log(f"Downloading {DOWNLOAD_URL} ([X])",section="AsyncDownloadManager")
        async with self.semaphore:
            async with session.get(DOWNLOAD_URL, allow_redirects=True, headers=self._headers) as response:
                HTTP_REQUEST_STATUS = response.status

                if HTTP_REQUEST_STATUS == 404 or HTTP_REQUEST_STATUS == 403:
                    raise FileNotFoundError('File not found')

                if DOWNLOAD_DIR != None and Path(DOWNLOAD_DIR).is_file():
                    logger.log(f"{DOWNLOAD_URL} already downloaded",section="AsyncDownloadManager")
                    return response

                start_time = time.time()
                queue_element.stat["downloaded"] = 0
                queue_element.stat["size"] = int(response.headers.get("Content-Length", 0))
                queue_element.stat["start_time"] = start_time
                if DOWNLOAD_DIR != None:
                    with open(DOWNLOAD_DIR, 'wb') as f:
                        async for chunk in response.content.iter_chunked(1024):
                            #await queue_element["pause_flag"].wait() TODO FIX !!!!!!!!!!!
                            f.write(chunk)

                            elapsed_time = time.time() - start_time
                            expected_time = len(chunk)
                            queue_element.stat["downloaded"] += expected_time
                            if queue_element.stat.get("size", 0) != 0:
                                queue_element.stat["percentage"] = (queue_element.stat.get("downloaded") / queue_element.stat.get("size")) * 100

                            for hook in self._hooks:
                                try:
                                    hook_dict = queue_element.copy()
                                    hook_dict["status"] = "downloading"

                                    hook(hook_dict)
                                except:
                                    pass
                            
                            if self.speed_limit_kbps:
                                expected_time = expected_time / (self.speed_limit_kbps * 1024)
                                if expected_time > elapsed_time:
                                    await asyncio.sleep(expected_time - elapsed_time)

                    for hook in self._hooks:
                        try:
                            hook_dict = queue_element.stat.copy()
                            hook_dict["status"] = "success"

                            hook(hook_dict)
                        except:
                            pass

                    logger.log(f"Successfully downloaded [0]",section="AsyncDownloadManager",kind=logger.KIND_SUCCESS)

                return response

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
