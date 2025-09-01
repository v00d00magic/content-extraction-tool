from .. import Implementation as Scratch
from declarable.Arguments import StringArgument

class Method(Scratch.AbstractExtractor):
    async def execute(self, i = {}):
        out = self.ContentUnit()
        out.content = i

        return [out]
