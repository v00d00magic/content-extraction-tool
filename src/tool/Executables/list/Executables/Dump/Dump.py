from Executables.Templates.Acts import Act
from Declarable.Arguments import ExecutableArgument, ObjectArgument
from DB.Models.Instances.ArgumentsDump import ArgumentsDump
from Utils.Data.JSON import JSON

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["executable"] = ExecutableArgument({})
        params["data"] = ObjectArgument({
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def implementation(self, i):
        dump = ArgumentsDump()
        if i.get("executable") != None:
            dump.executable = i.get("executable").getName()

        dump.data = JSON(i.get("data")).dump()
        dump.save()

        return dump.getStructure()
