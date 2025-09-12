from .. import Implementation as Scratch

class Implementation(Scratch.AbstractReceivation):
    executable_cfg =  {
        'free_args': True
    }

    async def implementation(self, i = {}):
        out = self.ContentUnit()
        out.content = i.__dict__()

        self.log("Written arguments")

        return [out]
