from executables.templates.representations import Representation
from declarable.Arguments import StringArgument, ObjectArgument

locale_keys = {
    "xml.name": {
        "en_US": "Xml"
    }
}

class Implementation(Representation):
    @classmethod
    def defineMeta(cls):
        return {
            "name": cls.key("xml.name"),
        }
