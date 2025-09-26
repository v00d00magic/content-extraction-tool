from Executables.templates.acts import Act
from App import app

locale_keys = {
    "name": {
        "en_US": "Display app info",
    },
}

class Implementation(Act):
    @classmethod
    def defineMeta(cls):
        return {
            'name': cls.key("name")
        }

    async def implementation(self, args = {}):
        return {
            "input": {
                "validated_args": args.__dict__(),
                "argv": app.argv,
            }
        }
