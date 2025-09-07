from .. import Implementation as Video
from declarable.Arguments import CsvArgument, StringArgument

class Implementation(Video.AbstractConfirmation):
    def declare(cls):
        params = {}
        params["url"] = CsvArgument({
            "orig": StringArgument({}),
            "default": None,
        })
        
        return params

    async def execute(self, i = {}):
        from submodules.Media.YtDlpWrapper import YtDlpWrapper

        output_args = self.outer_args

        with YtDlpWrapper({}).ydl as ydl:
            urls = i.get("url")
            print(urls)
            output_info = []

            for url in urls:
                _info = ydl.extract_info(url, download=False)

                if _info != None:
                    output_args.get("ids").get("default").append(_info.get("display_id"))

        return {
            "args": output_args
        }
