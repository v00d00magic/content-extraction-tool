from executables.templates.representations import Representation

locale_keys = {
    "text.name": {
        "en_US": "Text",
    }
}

class Implementation(Representation):
    @classmethod
    def define_meta(cls):
        return {
            "name": cls.key("text.name"),
        }
