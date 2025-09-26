from Executables.templates.extractors.Timeoutable import Timeoutable
from Executables.templates.extractors import Extractor
from Declarable.Arguments import IntArgument

import asyncio

class Implementation(Extractor, Timeoutable):
    @classmethod
    def declare(cls):
        params = {}
        params["start"] = IntArgument({
            "default": 1,
            "assertion": {
                "not_null": True,
            }
        })
        params["end"] = IntArgument({
            "default": 100,
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def implementation(self, i):
        for iterator in range(i.get("start"), i.get("end")):
            try:
                await self.iterate(i, iterator)
            except Exception as _e:
                app.logger.log(_e, "Iterable")

            await asyncio.sleep(i.get("timeout"))

    async def iterate(self, i = {})->list:
        pass
