from executables.templates.representations import Representation

locale_keys = {
    "json.name": {
        "en_US": "JSON"
    }
}

class Implementation(Representation):
    @classmethod
    def define_meta(cls):
        return {
            'name': cls.key("json.name")
        }
