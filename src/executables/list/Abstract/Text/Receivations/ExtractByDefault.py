from .. import Implementation as TextImplementation
from declarable.Arguments import StringArgument, CsvArgument
from utils.Data.Text import Text

class Implementation(TextImplementation.AbstractReceivation):
    @classmethod
    def declare(cls):
        params = {}
        params["text"] = CsvArgument({
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
            out.content = {
                'text': text
            }

            output.append(out)

        return output
