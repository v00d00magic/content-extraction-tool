from declarable.Arguments import ObjectArgument, LimitedArgument
from executables.templates.acts import Act
from resources.Consts import consts
from app.App import config

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
            return config.get("web.config_editing.allow")

        return super().canBeUsedAt(at)

    async def implementation(self, args = {}):
        values = args.get("values")
        tabu = consts.get("config.hidden_values_spaces")

        assert values != None, "new values not passed"

        for name, itm in values.items():
            val = values.get(name)
            no = False

            for _name in tabu:
                if name.startswith(_name):
                    no = True

            if no == True or val == None:
                continue

            config.set(name, val)

        return {
            "success": True
        }
