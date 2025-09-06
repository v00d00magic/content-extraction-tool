from executables.templates.extractors.Timeoutable import Timeoutable
from executables.templates.extractors.Iterable import Iterable
from executables.templates.extractors import Extractor
from declarable.Arguments import IntArgument
from resources.Exceptions import AbstractClassException
from app.App import logger
import math, asyncio

class BaseIterableExtended(Timeoutable, Iterable, Extractor):
    @classmethod
    def declare(cls):
        params = {}
        params["start_iteration"] = IntArgument({
            "default": 0
        })
        params["max_iteration"] = IntArgument({
            "default": 0
        })
        params["total_count"] = IntArgument({
            "default": None,
        })
        params["limit"] = IntArgument({
            "default": 0,
        })
        params["per_page"] = IntArgument({
            "default": 100
        })

        return params

    async def execute(self, i = {}):
        max_iteration = i.get('max_iteration')
        downloaded_count = 0
        output = []

        logger.log(message=f"Total {i.get('total_count')} items; will be {0} calls",section="Iterable!Extended", kind=logger.KIND_MESSAGE)

        for time in range(i.get('first_iteration'), i.get('call_times')):
            if max_iteration > 0 and time > max_iteration:
                return
            
            if i.get('limit_count') > 0 and (i.get('downloaded_count') > i.get('limit_count')):
                return

            logger.log(message=f"{time + 1}/{i.get('call_times')} time of items recieving",section="Iterable!Extended",kind=logger.KIND_MESSAGE)

            _items = await i.iterate(time)
            for _item in _items:
                downloaded_count += 1

                if i.get('limit') > 0:
                    if downloaded_count > i.get('limit_count'):
                        continue

                output.append(_item)

            if i.get("timeout") != 0:
                await asyncio.sleep(i.get("timeout"))

            return output
