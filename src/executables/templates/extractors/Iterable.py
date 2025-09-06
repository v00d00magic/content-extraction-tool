from app.App import logger
from executables.templates.extractors.Timeoutable import Timeoutable
from declarable.Arguments import IntArgument
import asyncio

class BaseIterable(Timeoutable):
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

    async def execute(self, i):
        for iterator in range(i.get("start"), i.get("end")):
            try:
                await self.iterate(i, iterator)
            except Exception as _e:
                logger.log(_e, "Iterable", silent=False)

            await asyncio.sleep(i.get("timeout"))

    async def iterate(self, i = {})->list:
        pass
