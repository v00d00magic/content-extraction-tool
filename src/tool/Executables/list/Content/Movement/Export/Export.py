from Executables.Templates.Acts import Act
from Declarable.Arguments import LimitedArgument, ClassArgument, ListArgument
from DB.Export.ArchiveExport import ArchiveExport
from DB.Export.ExportItem import ExportItem

class Implementation(Act):
    section_name = ["Export"]

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
            "default": "zip",
            "values": ["zip", "readable"],
        })

        return params

    async def implementation(self, i = {}):
        items = i.get("items")
        export_type = i.get("type")

        assert type(items) == list, "this is not a list"

        match (export_type):
            case "zip":
                self.log("Exporting as zip")

                export_manager = ArchiveExport()
                export_manager.defineTemp()
                export_manager.defineDB()

                for item in items:
                    try:
                        export_manager.export(item)
                    except AssertionError as e:
                        self.log_error(e)

                export_manager.end()

        return {}
