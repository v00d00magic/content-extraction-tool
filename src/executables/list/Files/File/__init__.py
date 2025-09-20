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
    @classmethod
    def defineMeta(cls):
        return {
            "name": cls.key("name"),
            "definition": cls.key("definition"),
        }

    @classmethod
    async def processItem(cls, item):
        return item

    @classmethod
    async def createSelf(cls, item):
        out = cls.ContentUnit()
        out.display_name = item.getFileName()
        out.JSONContent.update({})

        return out
