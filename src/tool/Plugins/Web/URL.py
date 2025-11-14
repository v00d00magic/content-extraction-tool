from Plugins.Web.DownloadManager.DownloadItem import DownloadItem
from Plugins.App.Executables.Types.Representation import Representation
from Plugins.App.Executables.Types.Act import Act
from Plugins.App.Executables.Types.Extractor import Extractor

from Plugins.Data.NameDictList import NameDictList
from Plugins.App.Arguments.Types.StringArgument import StringArgument
from Plugins.App.Arguments.Assertions.NotNoneAssertion import NotNoneAssertion

from urllib.parse import urlparse
import os, mimetypes
from App import app

class URL(Representation):
    @classmethod
    def define_data(cls):
        class NewContent(Representation.ContentUnit):
            class Data(Representation.ContentUnit.Data):
                url: str

            content: Data

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

        return NewContent

    class Submodules(Representation.Submodules):
        @property
        def manual_submodules(self) -> list:
            return ['ByString', 'Download']

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
                    item = URL.ContentUnit(
                        original_name = 'URL',
                        content = URL.ContentUnit.Data(
                            url = url
                        ),
                        source = URL.ContentUnit.Source(
                            types = "input",
                            content = "text"
                        )
                    )
                    item.flush(self.outer.call.get_db())

                    self.append(item)

        class Download(Act):
            submodule_value = "internal"

            class Execute(Extractor.Execute):
                async def implementation(self, i = {}) -> None:
                    url = i.get('url')
                    item = URL.ContentUnit(
                        original_name = 'URL',
                        content = URL.ContentUnit.Data(
                            url = url
                        ),
                        source = URL.ContentUnit.Source(
                            types = "input",
                            content = "text"
                        )
                    )
                    item.flush(self.outer.call.get_db())

                    self.append(item)
