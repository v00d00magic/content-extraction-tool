from executables.templates.acts import Act
from declarable.Arguments import ContentUnitArgument, CsvArgument

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["items"] = CsvArgument({
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
