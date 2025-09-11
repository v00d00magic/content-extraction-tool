from .. import Implementation as Video
from declarable.Arguments import CsvArgument, StringArgument

class Implementation(Video.AbstractConfirmation):
    @classmethod
    def declare(cls):
        params = {}
        params["url"] = CsvArgument({
            "orig": StringArgument({}),
            "default": None,
        })

        return params

    async def implementation(self, i = {}):
        from submodules.Media.YtDlpWrapper import YtDlpWrapper

        outer = self.outer.declare_recursive()
        with YtDlpWrapper({}).ydl as ydl:
            urls = i.get("url")
            for url in urls:
                _info = ydl.extract_info(url, download=False)
                if _info != None:
                    outer.get("ids").get("default").append(_info.get("display_id"))

        return {
            "args": outer
        }
