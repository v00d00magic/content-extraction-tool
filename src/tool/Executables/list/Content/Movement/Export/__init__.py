from Executables.Templates.Acts import Act
from Declarable.Arguments import LimitedArgument, ClassArgument, ListArgument
from DB.Export.ArchiveExport import ArchiveExport
from DB.Export.ExportItem import ExportItem

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["items"] = ListArgument({
            "orig": ClassArgument({
                "class": ExportItem
            }),
            "assertion": {
                "not_null": True
            }
        })
        params["type"] = LimitedArgument({
            "default": "archive",
            "values": ["archive", "readable"],
        })

        return params

    async def implementation(self, i = {}):
        items = i.get("items")
        assert type(items) == list, "this is not a list"

        print(items)
        # type:
        # archive - can be imported later
        # readable - cannot be imported, but can be seen by human eye

        '''export_type = i.get("type")
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

        return {}'''
