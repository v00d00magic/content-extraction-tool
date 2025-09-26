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
            return config.get("web.config_editing.allow")

        return super().canBeUsedAt(at)

    async def implementation(self, args = {}):
        values = args.get("values")
        tabu = config.hidden_items

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
