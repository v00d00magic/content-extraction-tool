from .. import Implementation as Json
from declarable.Arguments import StringArgument
from utils.MainUtils import parse_json

class Implementation(Json.AbstractReceivation):
    @classmethod
    def declare(cls):
        params = {}
        params["text"] = StringArgument({})

        return params

    async def implementation(self, i = {}):
        json_text = i.get('text')
        __obj = parse_json(json_text)

        out = self.ContentUnit()
        out.content = __obj

        return [out]
