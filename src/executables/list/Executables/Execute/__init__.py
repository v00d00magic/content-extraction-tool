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
        params["executable"] = ExecutableArgument({
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

        return params

    async def execute(self, i = {}):
        executable = i.get('executable')()
        is_save = i.get('is_save')
        links = i.get('link')
        is_confirmed = int(i.get("confirm")) == 1
        link_to = []

        if executable.isConfirmable() != None:
            args = executable.validate(executable.declare_recursive(), i.copy())

            if is_confirmed == False:
                pre_execute = executable.PreExecute(executable)
                new = await pre_execute.execute(args)
                pre_output = {
                    "tab": []
                }

                for arg_name, arg_item in new.get("args").items():
                    arg = new.get("args").get(arg_name)
                    if arg_name in pre_execute.args_list:
                        continue

                    new_object = arg.out()
                    new_object["name"] = arg_name

                    pre_output.get("tab").append(new_object)

                return pre_output

        if links != None and len(links) > 0:
            link_to = ContentUnit.ids(links)

        for link_item in link_to:
            executable.addLink(link_item)

        if getattr(executable, "beforeExecute", None) != None:
            executable.beforeExecute(i)

        result = await executable.execute(i)

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
