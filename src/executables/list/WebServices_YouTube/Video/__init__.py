from executables.templates.representations import Representation
from declarable.Arguments import CsvArgument, StringArgument
from utils.ClassProperty import classproperty

class Implementation(Representation):
    @classproperty
    def getRequiredModules(cls):
        return ["yt-dlp"]

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
