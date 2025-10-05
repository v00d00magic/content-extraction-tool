from Executables.Templates.Representations import Representation
from Declarable.Arguments import StringArgument, ObjectArgument

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
