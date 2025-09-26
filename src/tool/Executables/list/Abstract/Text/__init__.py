from Executables.Templates.Representations import Representation

locale_keys = {
    "text.name": {
        "en_US": "Text",
    }
}

class Implementation(Representation):
    @classmethod
    def defineMeta(cls):
        return {
            "name": cls.key("text.name"),
        }
