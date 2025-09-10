from executables.templates.acts import Act
from declarable.Arguments import LimitedArgument, JsonArgument, StringArgument
from db.Export.ArchiveExport import ArchiveExport

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["items"] = JsonArgument({
            "assertion": {
                "not_null": True
            },
            "docs": {
                "name": "acts.export.export.items.name",
            }
        })
        params["type"] = LimitedArgument({
            "default": "archive",
            "values": ["archive", "readable"],
            "docs": {
                "name": "acts.export.export.type.name",
            }
        })

        return params
    
    async def execute(self, i = {}):
        # Array of objects:
        # class — cu | su
        # id — id of item
        # flags:
        # Linked_depth (def: 0)

        items = i.get("items")
        assert type(items) == list, "this is not a list"

        # type:
        # archive - can be imported later
        # readable - cannot be imported, but can be seen by human eye

        export_type = i.get("type")
        to_export = []

        export_manager = ArchiveExport.create_manager()
        export_manager.define_temp()
        export_manager.define_db()

        for item in items:
            element_type = item.get("class")
            element_id = item.get("id")

            element_item = export_manager.getByTypeAndId(element_type, int(element_id))
            if element_item == None:
                continue

            _item = export_manager.getExportItem(element_item, item.get("flags"))
            _item.export()

        export_manager.end()

        return {}
