from Executables.templates.representations import Representation
from Declarable.Arguments import CsvArgument, StringArgument
from Utils.ClassProperty import classproperty

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
