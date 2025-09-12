from .. import Implementation as Scratch
from declarable.ExecutableConfig import ExecutableConfig

class Implementation(Scratch.AbstractReceivation):
    @classmethod
    def executable_cfg(cls):
        return ExecutableConfig({
            'free_args': True
        })

    async def implementation(self, i = {}):
        out = self.ContentUnit()
        out.content = i.__dict__()

        self.log("Written arguments")

        return [out]
