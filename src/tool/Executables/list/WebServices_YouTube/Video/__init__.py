from Executables.Templates.Representations import Representation
from Declarable.Arguments import ListArgument, StringArgument
from Utils.ClassProperty import classproperty

class Implementation(Representation):
    @classproperty
    def getRequiredModules(cls):
        return ["yt-dlp"]

    @classmethod
    def declare(cls):
        params = {}
        params["ids"] = ListArgument({
            "orig": StringArgument({}),
            "default": [],
            "assertion": {
                "not_null": True,
            }
        })

        return params
