from .. import Implementation as Json
from declarable.Arguments import StringArgument
from utils.Data.JSON import JSON

class Implementation(Json.AbstractReceivation):
    @classmethod
    def declare(cls):
        params = {}
        params["text"] = StringArgument({})

        return params

    async def implementation(self, i = {}):
        json_text = i.get('text')
        __obj = JSON(json_text).parse()

        out = self.ContentUnit()
        out.content = __obj

        return [out]
