from Plugins.Web.DownloadManager.DownloadItem import DownloadItem
from Plugins.App.Executables.Types.Representation import Representation
from Plugins.App.Executables.Types.Extractor import Extractor

from Plugins.Data.NameDictList import NameDictList
from Plugins.App.Arguments.Types.StringArgument import StringArgument
from Plugins.App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion

from urllib.parse import urlparse
import os, mimetypes
from App import app

class URL(Representation):
    class ContentUnit(Representation.ContentUnit):
        class ContentData(Representation.ContentUnit.ContentData):
            url: str

        content: ContentData

        async def download(self, download_to: str):
            return await app.download_manager.addDownload(DownloadItem(self.content.url, download_to))

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

    class Submodules(Representation.Submodules):
        class ByString(Extractor):
            submodule_value = "internal"
            
            class Arguments(Extractor.Arguments):
                @property
                def args(self) -> NameDictList:
                    return NameDictList([
                        StringArgument(
                            name = "url",
                            assertions = [
                                NotNoneAssertion()
                            ]
                        )
                    ])

            class Execute(Extractor.Execute):
                async def implementation(self, i = {}) -> None:
                    url = i.get('url')

                    self.append(self.outer.parent.saver.ContentUnit(
                        original_name = 'URL',
                        content = URL.ContentUnit.ContentData(
                            url = url
                        ),
                        source = URL.ContentUnit.Source(
                            types = "input",
                            content = "text"
                        )
                    ))
