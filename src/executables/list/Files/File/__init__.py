from executables.templates.representations import Representation

locale_keys = {
    "name": {
        "en_US": "File"
    },
    "definition": {
        "en_US": "File by path or URL",
    },
}

class Implementation(Representation):
    # Class for testing purposes

    @classmethod
    def define_meta(cls):
        return {
            "name": cls.key("name"),
            "definition": cls.key("definition"),
        }

    @staticmethod
    async def process_item(item):
        return item
