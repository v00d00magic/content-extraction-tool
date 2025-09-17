from .. import Implementation as Json
from declarable.Arguments import ObjectArgument
from utils.Data.List import List

class Implementation(Json.AbstractReceivation):
    @classmethod
    def declare(cls):
        params = {}
        params["object"] = ObjectArgument({
            "type": "object",
        })

        return params

    async def implementation(self, i = {}):
        json_object = List(i.get('object')).convert()
        outs = []
        
        for i in json_object:
            out = self.ContentUnit()
            out.content = i

            outs.append(out)

        return outs

