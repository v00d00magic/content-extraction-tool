from declarable.Arguments import CsvArgument, StringArgument
from .. import Implementation as File
from utils.Web.URL import URL
from pathlib import Path

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
        outs = []

        for _url in i.get('url'):
            url = URL(_url)

            out = self.ContentUnit()
            out_file = self.StorageUnit()

            tmp_dir = out_file.Temp.get()
            common_file_path = tmp_dir.joinpath("download.tmp")

            # Making HTTP request
            request = await url.download(common_file_path)

            result_name = '.'.join(url.getNames(request))
            result_path = tmp_dir.joinpath(result_name)

            common_file_path.rename(result_path)
            out_file.fillByPath(result_path)
            out_file.flush()

            out.link(out_file, True)
            out.display_name = result_name
            out.Source.update({
                'type': 'url',
                'content': _url
            })
            out.JSONContent.update({})
            out = await self.outer.process_item(out)

            outs.append(out)

        return outs
