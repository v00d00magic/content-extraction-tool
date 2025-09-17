from executables.templates.acts import Act
from app.App import config

class Implementation(Act):
    @classmethod
    def canBeUsedAt(cls, at):
        if at == "web":
            return config.get("web.config_editing.allow")

        return super().canBeUsedAt(at)

    async def implementation(self, args = {}):
        result = []

        for name, itm in config.compared_options.items():
            val = config.compared_options.get(name)
            no = False

            for _name in config.hidden_items:
                if name.startswith(_name):
                    no = True

            if no == True:
                continue

            val.configuration["name"] = name
            val.configuration["current"] = config.options.get(name)

            result.append(val.getStructure())

        return result
