from ..Collection import Implementation as Collection
from Declarable.Arguments import StringArgument

class Implementation(Collection.AbstractReceivation):
    @classmethod
    def declare(cls):
        params = {}
        params["name"] = StringArgument({
            'assertion': {
                'not_null': True
            }
        })
        params["description"] = StringArgument({
            'is_long': True,
        })

        return params

    async def implementation(self, i = {}):
        # not self.Collection() !
        out = self.ContentUnit()
        out.content = {}
        out.display_name = i.get('name')
        out.description = i.get('description')
        out.is_collection = True

        await out.flush()

        self.variable("items").append(out)
