from .. import Implementation as Text
from Declarable.Arguments import StringArgument
from Utils.Data.JSON import JSON

class Implementation(Text.AbstractReceivation):
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
