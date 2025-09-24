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

            out_file = self.StorageUnit()

            common_file = out_file.getDir().joinpath("download.tmp")

            request = await url.download(common_file)

            out_file.setCommonFile(common_file)
            out_file.setName(url.getNameAndExtensionByRequest(request))
            out_file.clearCommonFile()
            await out_file.flush()

            out = self.ContentUnit()
            out.display_name = out_file.getFileName()
            out.JSONContent.update({})
            out.Source.update({
                'type': 'url',
                'content': _url
            })

            await out.flush()
            out.LinkManager.linkAsCommon(out_file)

            outs.append(out)

        return outs
