from .. import Implementation as Scratch

class Implementation(Scratch.AbstractReceivation):
    async def execute(self, i = {}):
        out = self.ContentUnit()
        out.content = i

        return [out]
