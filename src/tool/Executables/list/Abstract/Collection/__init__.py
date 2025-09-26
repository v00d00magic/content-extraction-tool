from Executables.Templates.Representations import Representation

locale_keys = {
    "collection.name": {
        "en_US": "Collection",
    },
}

class Implementation(Representation):
    @classmethod
    def defineMeta(cls):
        return {
            "name": cls.key("collection.name"),
        }
