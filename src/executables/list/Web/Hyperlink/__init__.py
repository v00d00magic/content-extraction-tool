from executables.templates.representations import Representation

locale_keys = {
    "hyperlink.name": {
        "en_US": "Hyperlink",
        "ru_RU": "Ссылка"
    },
    "hyperlink.definition": {
        "en_US": "Hyperlink to web-site",
        "ru_RU": "Ссылка на web-ресурс"
    }
}

class Implementation(Representation):
    @classmethod
    def define_meta(cls):
        return {
            "definition": cls.key("hyperlink.definition"),
            "name": cls.key("hyperlink.name"),
        }
