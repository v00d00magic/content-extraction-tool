from Executables.templates.representations import Representation

locale_keys = {
    "arguments.name": {
        "en_US": "Passed data",
    }
}

class Implementation(Representation):
    @classmethod
    def defineMeta(cls):
        return {
            "name": cls.key("arguments.name"),
        }
