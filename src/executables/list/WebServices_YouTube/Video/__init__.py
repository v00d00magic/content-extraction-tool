from executables.templates.representations import Representation
from executables.templates.Confirmable import Confirmable
from declarable.Arguments import CsvArgument, StringArgument

class Implementation(Representation):
    required_modules = ["yt-dlp"]
    executable_cfg = {
        "variants": []
    }

    @classmethod
    def declare(cls):
        params = {}
        params["url"] = CsvArgument({
            "orig": StringArgument({}),
            "default": None,
        })
        params["ids"] = CsvArgument({
            "orig": StringArgument({}),
            "default": [],
            "assertion": {
                "not_null": True,
            }
        })

        return params

    class PreExecute(Confirmable.PreExecute):
        args_list = ["url"]

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
