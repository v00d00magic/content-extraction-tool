from .. import Implementation as TextImplementation
from Declarable.Arguments import StringArgument, ListArgument
from Utils.Data.Text import Text

class Implementation(TextImplementation.AbstractReceivation):
    @classmethod
    def declare(cls):
        params = {}
        params["text"] = ListArgument({
            "orig": StringArgument({
                "is_long": True,
            }),
            "default": None,
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def implementation(self, i = {}):
        texts = i.get('text')
        output = []

        for text in texts:
            out = self.ContentUnit()
            out.display_name = Text(text).cut(100)
            out.JSONContent.update({
                'text': text
            })
            await out.flush()

            output.append(out)

        return output
