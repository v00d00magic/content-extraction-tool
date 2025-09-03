from declarable.Arguments import LimitedArgument
from executables.templates.acts import Act
from app.App import app

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["type"] = LimitedArgument({
            "values": ['representation', 'act', 'service'],
        })

        return params

    async def execute(self, i = {}):
        lists = app.indexated_scripts.items_by_class(i.get("type"))
        fnl = []
        for item in lists:
            try:
                fnl.append(item.describe())
            except ModuleNotFoundError:
                pass
            except Exception as e:
                print(e)
                raise e

        return fnl
