
from pydantic import Field, computed_field

from Objects.Hookable import Hookable
from Objects.Object import Object
from Objects.Configurable import Configurable
from Objects.Increment import Increment
from Objects.ClassProperty import classproperty

from Plugins.Data.NameDictList import NameDictList
from Plugins.Web.Http.Headers import Headers
from .DownloadManagerItems import DownloadManagerItems
from .DownloadItem import DownloadItem
from typing import Type

import asyncio, aiohttp
from App import app

class DownloadManager(Object, Hookable, Configurable):
    max_concurrent_downloads: int = Field(default = 3)
    max_kbps_speed: int = Field(default = None)
    connection_timeout: int = Field(default = 10)

    semaphore: Type[asyncio.Semaphore] = None
    timeout: Type[aiohttp.ClientTimeout] = None
    session: Type[aiohttp.ClientSession] = None
    queue: DownloadManagerItems = None
    downloads: Type[Increment] = None

    inited: bool = False

    def _constructor(self):
        self.semaphore = asyncio.Semaphore(self.max_concurrent_downloads)
        self.timeout = aiohttp.ClientTimeout(total=self.connection_timeout)
        self.session = aiohttp.ClientSession(timeout = self.timeout)
        self.queue = DownloadManagerItems(manager = self)
        self.downloads = Increment()

        self.inited = True

    async def add(self, item: DownloadItem) -> aiohttp.ClientResponse:
        if self.inited == False:
            self._constructor()

        self.queue.append(item)

        results = await item.start()

        self.queue.remove(item)

        return results

    @property
    @computed_field
    def headers(self):
        headers = Headers(
            user_agent = app.Config.get("net.useragent")
        )

        return headers.model_dump(by_alias = True)

    @property
    def section_name(self) -> list:
        return ["DownloadManager"]

    @classproperty
    def options(cls) -> NameDictList:
        from Plugins.App.Arguments.Types.StringArgument import StringArgument
        from Plugins.App.Arguments.Types.IntArgument import IntArgument

        return NameDictList([
            IntArgument(
                name = "media.download_manager.max_concurrent_downloads",
                default = 3,
            ),
            IntArgument(
                name = "media.download_manager.max_kbps_speed",
                default = 2000,
            ),
            IntArgument(
                name = "media.download_manager.connection_timeout",
                default = 100
            ),
            StringArgument(
                name = "media.download_manager.user_agent",
                default = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
            ),
        ])
