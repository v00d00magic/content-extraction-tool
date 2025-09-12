from executables.templates.acts import Act
from app.App import app

locale_keys = {
    "name": {
        "ru_RU": "Отображение информации",
        "en_US": "App info display",
    },
}

class Implementation(Act):
    @classmethod
    def define_meta(cls):
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
