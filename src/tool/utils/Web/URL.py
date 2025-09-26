from urllib.parse import urlparse
import os, mimetypes
from utils.Web.DownloadManager import DownloadManagerItem
from app.App import download_manager

class URL():
    def __init__(self, url):
        self._orig = url
        self.url = urlparse(url)

    async def download(self, download_to: str):
        return await download_manager.addDownload(DownloadManagerItem(self._orig, download_to))

    def getNameAndExtensionByRequest(self, request):
        content_type = request.headers.get('Content-Type', '').lower()
        mime_ext = mimetypes.guess_extension(content_type)

        path = self.url.path
        if path.endswith('/') or path == "":
            return "index", "html"

        filename = os.path.basename(path)
        name, ext = os.path.splitext(filename)
        if not ext:
            if mime_ext:
                ext = mime_ext[1:]
        else:
            ext = ext[1:]

        return name, ext
