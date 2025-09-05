from executables.templates.acts import Act
from db.Models.Content.ContentUnit import ContentUnit
from declarable.Arguments import JsonArgument, CsvArgument

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["items"] = CsvArgument({
            "orig": JsonArgument({}),
            "assertion": {
                "not_null": True
            }
        })

        return params

    async def execute(self, i = {}):
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
