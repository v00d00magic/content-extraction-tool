from executables.templates.representations import Representation

locale_keys = {
    "json.name": {
        "en_US": "JSON"
    }
}

class Implementation(Representation):
    @classmethod
    def defineMeta(cls):
        return {
            'name': cls.key("json.name")
        }
