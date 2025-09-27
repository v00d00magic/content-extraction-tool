from Executables.Templates.Acts import Act
from App import app

class Implementation(Act):
    @classmethod
    def canBeUsedAt(cls, at):
        if at == "web":
            return app.config.get("config.external_editing.allow")

        return super().canBeUsedAt(at)

    async def implementation(self, args = {}):
        result = []

        for name, itm in app.config.compared_options.items():
            option = app.config.compared_options.get(name)

            if app.config.isItemHidden(name) == True:
                continue

            option.data["name"] = name
            option.data["current"] = app.config.options.get(name)

            result.append(option.getStructure())

        return result
