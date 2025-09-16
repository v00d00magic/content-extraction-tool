from executables.templates.representations import Representation

locale_keys = {
    "arguments.name": {
        "en_US": "Passed data",
    }
}

class Implementation(Representation):
    @classmethod
    def define_meta(cls):
        return {
            "name": cls.key("arguments.name"),
        }
