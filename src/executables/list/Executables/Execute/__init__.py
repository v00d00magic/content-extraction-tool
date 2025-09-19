from declarable.Arguments import CsvArgument, ContentUnitArgument, ExecutableArgument, BooleanArgument
from executables.responses.Response import Response
from executables.templates.acts import Act
from db.Models.Content.ContentUnit import ContentUnit
from declarable.ExecutableConfig import ExecutableConfig
from executables.ExecutableCall import ExecutableCall

locale_keys = {
    "name": {
        "en_US": "Link to",
    }
}

class Implementation(Act):
    @classmethod
    def executable_cfg(cls):
        return ExecutableConfig({
            'free_args': True
        })

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
                "name": Act.key("name"),
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
            "default": False
        })
        params["ignore_requirements"] = BooleanArgument({
            'default': False,
        })

        return params

    async def implementation(self, i = {}):
        executable = i.get('i')

        assert executable.canBeExecuted(), "sorry!"

        if i.get("dump") == True:
            self.call.dump()

        if i.get("ignore_requirements") == False:
            assert executable.isModulesInstalled(), "requirements not installed"

        def __progress_hook(message):
            self.trigger("progress", message=message)

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
                    _out["args"][item_name] = item.getStructure()

                return _out

        link_to = []
        links = i.get('link')
        if links != None and len(links) > 0:
            link_to = ContentUnit.ids(links)

        _pass = i.__dict__(self.__class__.declare().keys())

        this_call = ExecutableCall(executable=executable)
        #this_call.add_hook("progress", __progress_hook)
        for link_item in link_to:
            this_call.addLink(link_item)

        this_call.passArgs(_pass)
        result = await this_call.run_asyncely()

        if hasattr(result, "items") == True:
            for item in result.items():
                if i.get('is_save') == True:
                    await item.flush()
                    this_call.doLink(item)

        return result
