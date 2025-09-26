from Declarable.Arguments import ListArgument, ContentUnitArgument, ExecutableArgument, BooleanArgument
from Executables.Responses.Response import Response
from Executables.Responses.ItemsResponse import ItemsResponse
from Executables.Templates.Acts import Act
from DB.Models.Content.ContentUnit import ContentUnit
from Declarable.ExecutableConfig import ExecutableConfig
from Executables.ExecutableCall import ExecutableCall
from App import app

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
        params["links"] = ListArgument({
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
            assert executable.isModulesInstalled(), "requirements not satisfied"

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

        result = await this_call.run_asyncely()
        for link in this_call.getCollections():
            link_to.append(link)

        if isinstance(result, ItemsResponse) == True:
            if is_save == True:
                items = result.items()

                app.logger.log(f"Moving {len(items)} to common db", section=["Executables", "DBMovement"])

                for item in items:
                    app.logger.log(f"Moving {item.name_db_id} to common db", section=["Executables", "DBMovement"])

                    item.moveToDb(app.db_connection.db)
                    #item.linkTo(link_to)

        return result
