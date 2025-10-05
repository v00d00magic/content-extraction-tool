from Executables.Templates.Representations import Representation

locale_keys = {
    "name": {
        "en_US": "File"
    },
    "definition": {
        "en_US": "File by path or URL",
    },
}

class Implementation(Representation):
    @classmethod
    def defineMeta(cls):
        return {
            "name": cls.key("name"),
            "definition": cls.key("definition"),
        }
