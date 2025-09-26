from declarable.Arguments import LimitedArgument
from executables.templates.acts import Act
from app.App import app

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
