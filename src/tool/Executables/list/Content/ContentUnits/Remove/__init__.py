from Executables.Templates.Acts import Act
from Declarable.Arguments import ContentUnitArgument, ListArgument

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["items"] = ListArgument({
            "orig": ContentUnitArgument({}),
            "assertion": {
                "not_null": True
            }
        })

        return params

    async def implementation(self, i = {}):
        items = i.get("items")
        successes = 0

        for item in items:
            if item == None:
                continue

            item.delete_instance()
            successes += 1

        return {
            "removed": successes
        }
