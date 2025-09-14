from declarable.Arguments import CsvArgument, StringArgument
from .. import Implementation as File
from utils.WebUtils import is_generated_ext
from pathlib import Path
from submodules.Web.classes.URL import URL

locale_keys = {
    "url.name": {
        "en_US": "URL"
    }
}

class Implementation(File.AbstractReceivation):
    @classmethod
    def declare(cls):
        params = {}
        params["url"] = CsvArgument({
            "docs": {
                "name": cls.key("url.name")
            },
            "orig": StringArgument({}),
            "default": None,
        })

        return params
    
    async def implementation(self, i = {}):
        from submodules.Web.DownloadManager import download_manager
        import mimetypes, os

        outs = []

        for _url in i.get('url'):
            url = URL(_url)

            out = self.ContentUnit()
            out_file = self.StorageUnit()

            tmp_dir = out_file.temp_dir
            tmp_path = Path(os.path.join(tmp_dir, "download.tmp"))
            result_name = '.'.join([name, ext])
            result_path = Path(os.path.join(tmp_dir, result_name))

            # Making HTTP request

            url_request = await download_manager.addDownload(end = url,dir = tmp_path)

            header_content_type = url_request.headers.get('Content-Type', '').lower()
            mime_ext = None
            if ext == '' or is_generated_ext(ext):
                mime_ext = mimetypes.guess_extension(header_content_type)
                if mime_ext:
                    ext = mime_ext[1:]
                else:
                    ext = 'html'

            result_name = '.'.join([name, ext])
            result_path = Path(os.path.join(tmp_dir, result_name))
            tmp_path.rename(os.path.join(tmp_dir, result_path))

            out_file.writeData({
                "extension": ext,
                "upload_name": result_name,
                "filesize": result_path.stat().st_size,
            })

            out.link(out_file, True)
            out.display_name = result_name
            out.Source.update({
                'type': 'url',
                'content': url
            })
            out.JSONContent.update({})
            out = await self.outer.process_item(out)

            outs.append(out)

        return outs
