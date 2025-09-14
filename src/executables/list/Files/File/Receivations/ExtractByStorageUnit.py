from declarable.Arguments import CsvArgument, StorageUnitArgument
from .. import Implementation as File

locale_keys = {
    "storage_unit.name": {
        "en_US": "Storage unit ID"
    }
}

class Implementation(File.AbstractReceivation):
    @classmethod
    def declare(cls):
        params = {}
        params["storage_unit"] = CsvArgument({
            "orig": StorageUnitArgument({}),
            "docs": {
                "name": cls.key("storage_unit.name")
            },
        })

        return params

    async def implementation(self, i = {}):
        outs = []

        for item in i.get('storage_unit'):
            if item == None:
                continue

            out = self.ContentUnit()

            out.link(item, True)
            out = await self.outer.process_item(out)

            outs.append(out)

        return outs
