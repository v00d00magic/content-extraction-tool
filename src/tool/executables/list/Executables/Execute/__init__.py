from declarable.Arguments import CsvArgument, ContentUnitArgument, ExecutableArgument, BooleanArgument
from executables.responses.Response import Response
from executables.responses.ItemsResponse import ItemsResponse
from executables.templates.acts import Act
from db.Models.Content.ContentUnit import ContentUnit
from declarable.ExecutableConfig import ExecutableConfig
from executables.ExecutableCall import ExecutableCall
from app.App import db_connection

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
        params["links"] = CsvArgument({
            "orig": ContentUnitArgument({}),
            "docs": {
                "name": Act.key("name"),
            },
            "default": []
        })
        params["create_internal_collections"] = BooleanArgument({
            "default": False
        })
        params["save_all"] = BooleanArgument({
            "default": True
        })
        params["confirm"] = BooleanArgument({
            "default": True
        })
        params["dump"] = BooleanArgument({
            "default": False
        })
        params["check_requirements"] = BooleanArgument({
            'default': True,
        })

        return params

    async def implementation(self, i = {}):
        executable = i.get('i')
        is_save = i.get('save_all')
        links = i.get('links')

        assert executable.canBeExecuted(), "sorry!"

        if i.get("dump") == True:
            self.call.dump()

        if i.get("check_requirements") == True:
            assert executable.isModulesInstalled(), "requirements not installed"

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
        if links != None and len(links) > 0:
            for link in ContentUnit.ids(links):
                link_to.append(link)

        this_call = ExecutableCall(executable=executable)
        this_call.passArgs(i.__dict__(exclude=self.__class__.declare().keys()))

        await this_call.run_asyncely()
        for link in this_call.getCollections():
            link_to.append(link)

        if isinstance(this_call.getResult(), ItemsResponse) == True:
            for item in result.items():
                if is_save == True:
                    item.moveToDb(db_connection.db)
                    #item.linkTo(link_to)

        return result
