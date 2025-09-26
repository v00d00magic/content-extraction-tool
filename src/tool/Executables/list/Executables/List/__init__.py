from Declarable.Arguments import LimitedArgument
from Executables.Templates.Acts import Act
from App import app

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["type"] = LimitedArgument({
            "values": ['Representation', 'Act', 'Service', 'Extractor'],
        })

        return params

    async def implementation(self, i = {}):
        fnl = []
        for item in app.indexated_scripts.listByClass(i.get("type")):
            try:
                fnl.append(item.getStructure())
            except ModuleNotFoundError:
                pass

        return fnl
