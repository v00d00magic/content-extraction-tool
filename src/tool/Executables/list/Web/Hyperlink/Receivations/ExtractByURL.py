from .. import Implementation as Hyperlink
from Declarable.Arguments import ListArgument

class Implementation(Hyperlink.AbstractAct):
    @classmethod
    def declare(cls):
        params = {}
        params["url"] = ListArgument({
            "default": None,
        })

        return params

    async def implementation(self, i = {}):
        urls = i.get('url')
        outs = []

        for url in urls:
            out = self.ContentUnit()
            out.content = {
                'url': str(url),
            }
            # TODO add opengraph parse

            outs.append(out)

        return outs
