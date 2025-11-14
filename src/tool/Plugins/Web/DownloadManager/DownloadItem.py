from pathlib import Path
from Objects.Object import Object
from Plugins.App.Logger.LogParts.LogPrefix import LogPrefix
from pydantic import Field
from enum import Enum
from typing import Type
import os, time, asyncio, aiohttp

# i think it is dataclass ??
class DownloadManagerItemStat():
    downloaded: int = 0
    total_size: int = 0
    started_at: float = None

    def getPercentage(self):
        return (self.downloaded / self.total_size) * 100

    def getRemainingTime(self):
        return 0

class DownloadManagerItemStatusEnum(Enum):
    end = "end"
    downloading = "downloading"
    started = "started"
    unknown = "unknown"

class DownloadItem(Object):
    manager: Object = Field(default=None)
    url: str = Field(default=None)
    save_to: Path = Field(default=None)
    status: DownloadManagerItemStatusEnum = Field(default=DownloadManagerItemStatusEnum.unknown.value)

    id: int = 0
    task: Type[asyncio.Task] = None

    def _constuctor(self):
        self.pause_flag = asyncio.Event()
        self.stat = DownloadManagerItemStat()
        self.id = self.manager.downloads.getIndex()

    def pause(self, url):
        self.pause_flag.set()

    def resume(self, url):
        self.pause_flag.clear()

    async def start(self):
        async with self.manager.session as session:
            self.log(f"Started download. URL: {self.url}")
            self.stat.started_at = time.time()
            self.task = await asyncio.create_task(self.download(session))

            return self.task

    async def download(self, session):
        async with self.manager.semaphore:
            request = session.get(self.url, allow_redirects=True, headers=self.manager.headers)
            async with request as response:
                status = response.status

                if status in [404, 403]:
                    # if self.manager.ignore_codes in 404 or idk
                    self.log_error("File returned 404")
                    raise FileNotFoundError('File not found')

                content_length = int(response.headers.get("Content-Length", 0))
                self.stat.downloaded = 0

                if content_length != None:
                    self.stat.total_size = content_length

                if self.save_to != None:
                    assert self.save_to.is_file() == False, "file with this name already exists"

                    await self.saveToFile(response, self.save_to)
                else:
                    self.log("Did not saving cuz save_to is not passed!")

                self.status = "success"
                self.manager.trigger("success", self)
                self.log_success(f"Download complete")

                return response

    async def saveToFile(self, response: aiohttp.ClientResponse, save_dir: Path):
        response_iter_per = 1024
        is_dir = save_dir.is_dir()

        with open(self.save_to, 'wb') as stream:
            async for chunk in response.content.iter_chunked(response_iter_per):
                await self.pause_flag.wait()

                stream.write(chunk)

                now = time.time()
                elapsed_time = now - self.start_time
                chunk_length = len(chunk)
                print(chunk_length)

                self.stat.downloaded += chunk_length
                self.status = DownloadManagerItemStatusEnum.downloading.value
                self.manager.trigger("downloading", self)

                if self.manager.max_kbps_speed:
                    expected_time = chunk_length / (self.max_kbps_speed)
                    if expected_time > elapsed_time:
                        await asyncio.sleep(expected_time - elapsed_time)

    @property
    def append_prefix(self) -> LogPrefix:
        return LogPrefix(name = "DownloadItem", id = self.id)
