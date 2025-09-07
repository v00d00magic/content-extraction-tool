from declarable.Arguments import CsvArgument, StorageUnitArgument
from .. import Implementation as File

keys = {
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
                "name": keys.get("storage_unit.name")
            },
        })

        return params

    async def execute(self, i = {}):
        su = i.get('storage_unit')
        outs = []

        for item in su:
            if item == None:
                continue

            out = self.ContentUnit()

            out.addLink(item)
            out.setCommonLink(item)
            out = await self.outer.process_item(out)

            outs.append(out)

        return outs
