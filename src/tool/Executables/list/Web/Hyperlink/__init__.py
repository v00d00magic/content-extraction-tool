from Executables.templates.representations import Representation

locale_keys = {
    "hyperlink.name": {
        "en_US": "Hyperlink",
    },
    "hyperlink.definition": {
        "en_US": "Hyperlink to web-site",
    }
}

class Implementation(Representation):
    @classmethod
    def defineMeta(cls):
        return {
            "definition": cls.key("hyperlink.definition"),
            "name": cls.key("hyperlink.name"),
        }
