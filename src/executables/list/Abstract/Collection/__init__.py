from executables.templates.representations import Representation

locale_keys = {
    "collection.name": {
        "en_US": "Collection",
    },
}

class Implementation(Representation):
    @classmethod
    def define_meta(cls):
        return {
            "name": cls.key("collection.name"),
        }
