from Executables.templates.acts import Act
from Declarable.Arguments import ExecutableArgument

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["class"] = ExecutableArgument({
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def implementation(self, i = {}):
        return i.get('class').getStructure()
