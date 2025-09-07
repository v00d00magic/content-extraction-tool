from executables.templates.representations import Representation
from declarable.Arguments import CsvArgument, StringArgument

class Implementation(Representation):
    required_modules = ["yt-dlp"]
    executable_cfg = {
        "variants": []
    }

    @classmethod
    def declare(cls):
        params = {}
        params["ids"] = CsvArgument({
            "orig": StringArgument({}),
            "default": [],
            "assertion": {
                "not_null": True,
            }
        })

        return params
