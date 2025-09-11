from declarable.Arguments import CsvArgument, ContentUnitArgument, ExecutableArgument, BooleanArgument
from executables.responses.Response import Response
from executables.list.Executables.Dump import Implementation as Dump
from executables.templates.acts import Act
from db.Models.Content.ContentUnit import ContentUnit

keys = {
    "name": {
        "en_US": "Link to",
        "ru_RU": "Привязать к",
    }
}

class Implementation(Act):
    executable_cfg = {
        'free_args': True
    }

    @classmethod
    def declare(cls):
        params = {}
        params["i"] = ExecutableArgument({
            "assertion": {
                "not_null": True,
                "can_be_executed": True
            }
        })
        params["link_after"] = CsvArgument({
            "orig": ContentUnitArgument({}),
            "docs": {
                "name": keys.get("name"),
            },
            "default": []
        })
        params["is_save"] = BooleanArgument({
            "default": True
        })
        params["confirm"] = BooleanArgument({
            "default": True
        })
        params["dump"] = BooleanArgument({
            "default": True
        })
        params["ignore_requirements"] = BooleanArgument({
            'default': False,
        })

        return params

    async def implementation(self, i = {}):
        executable = i.get('i')(self.index)
        links = i.get('link')
        link_to = []
        _pass = i.__dict__()
        _pass.pop("i")

        def __progress_hook(message):
            self.trigger("progress", message=message)

        executable.add_hook("progress", __progress_hook)

        if i.get("dump") == True:
            await Dump().execute({
                "executable": executable,
                "data": _pass
            })

        if i.get("ignore_requirements") == False:
            assert executable.isModulesInstalled(), f"requirements not installed. run 'Executables.InstallRequirements'"

        if len(executable.confirmations) > 0:
            if int(i.get("confirm")) == 1 == False:
                res = await executable.confirmations[0]().execute_with_validation(i)
                _out = {
                    "preferred_receivation": None,
                    "args": {},
                    "data": {},
                }
                _out["data"] = res.get("data")
                for item_name, item in res.get("args").items():
                    _out["args"][item_name] = item.describe()

                return _out

        if links != None and len(links) > 0:
            link_to = ContentUnit.ids(links)

        for link_item in link_to:
            executable.addLink(link_item)

        if getattr(executable, "beforeExecute", None) != None:
            executable.beforeExecute(i)

        result = Response.convert(await executable.execute_with_validation(_pass))
        if hasattr(result, "items") == True:
            for item in result.items():
                if i.get('is_save') == True:
                    item.save()
                    executable.doLink(item)

        return result
