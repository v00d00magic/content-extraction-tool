from executables.templates.acts import Act
from db.Models.Content.ContentUnit import ContentUnit
from declarable.Arguments import CsvArgument, ContentUnitArgument, ExecutableArgument, BooleanArgument

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
        params["ignore_requirements"] = BooleanArgument({
            'default': False,
        })

        return params

    async def execute(self, i = {}):
        executable = i.get('i')(self.index)
        is_save = i.get('is_save')
        links = i.get('link')
        is_skip_confirmation = int(i.get("confirm")) == 1
        link_to = []
        ignore_requirements = i.get("ignore_requirements")
        _pass = i.__dict__()
        _pass.pop("i")

        def __progress_hook(message):
            self.trigger("progress", message=message)

        executable.add_hook("progress", __progress_hook)

        if ignore_requirements == False:
            assert executable.isModulesInstalled(), f"requirements not installed. run 'Executables.InstallRequirements'"

        if len(executable.confirmations) > 0:
            if is_skip_confirmation == False:
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

        result = await executable.execute_with_validation(_pass)

        if executable.self_name in ["Extractor", "Receivation", "Representation"]:
            output = []

            for item in result:
                if is_save == True:
                    item.save()
                    executable.doLink(item)

                output.append(item.getStructure())

            return {
                "items": output
            }

        return result
