from executables.templates.acts import Act
from declarable.Arguments import ExecutableArgument, ObjectArgument
from db.Models.Instances.ArgumentsDump import ArgumentsDump
from utils.MainUtils import dump_json

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
            dump.executable = i.get("executable").full_name()

        dump.data = dump_json(i.get("data"))
        dump.save()

        return dump.getStructure()
