from Executables.Templates.Acts import Act
from DB.Models.Content.ContentUnit import ContentUnit
from Declarable.Arguments import JsonArgument, ListArgument

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["items"] = ListArgument({
            "orig": JsonArgument({}),
            "assertion": {
                "not_null": True
            }
        })

        return params

    async def implementation(self, i = {}):
        items = i.get('items')
        out_items = []
        results = []

        for item in items:
            _id = item.get("uuid")
            _name = item.get("name")
            
            unit = ContentUnit.ids(_id)
            if _name != None:
                unit.display_name = _name

            out_items.append(unit)

        for item in out_items:
            results.append(item.getStructure())

        return results
