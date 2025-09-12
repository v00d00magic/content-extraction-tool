from executables.templates.representations import Representation

locale_keys = {
    "name": {
        "ru_RU": "Файл",
        "en_US": "File"
    },
    "definition": {
        "ru_RU": "Файл по пути на диске или URL",
        "en_US": "File by filepath or URL",
    },
}

class Implementation(Representation):
    @classmethod
    def define_meta(cls):
        return {
            "name": cls.key("name"),
            "definition": cls.key("definition"),
        }

    @staticmethod
    async def process_item(item):
        return item
