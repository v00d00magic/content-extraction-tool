from Declarable.Arguments import ObjectArgument, LimitedArgument
from Executables.Templates.Acts import Act
from App import app

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["values"] = ObjectArgument({
            "assertion": {
                "not_null": True,
            }
        })

        return params

    @classmethod
    def canBeUsedAt(cls, at):
        if at == "web":
            return app.config.get("config.external_editing.allow")

        return super().canBeUsedAt(at)

    async def implementation(self, args = {}):
        values = args.get("values")

        assert values != None, "new values not passed"

        for name, itm in values.items():
            val = values.get(name)

            if app.config.isItemHidden(name) or val == None:
                continue

            app.config.set(name, val)

        return {
            "success": True
        }
