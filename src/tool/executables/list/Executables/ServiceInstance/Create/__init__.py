from Executables.templates.acts import Act
from Executables.templates.services import Service
from DB.Models.Instances.ServiceInstance import ServiceInstance
from Declarable.Arguments import StringArgument, IntArgument
from Declarable.ExecutableConfig import ExecutableConfig

class Implementation(Act):
    @classmethod
    def executable_cfg(cls):
        return ExecutableConfig({
            'free_args': True
        })

    @classmethod
    def declare(cls):
        params = {}
        params["class"] = StringArgument({
            "assertion": {
                "not_null": True,
            }
        })
        params["display_name"] = StringArgument({})
        params["interval"] = IntArgument({
            "default": 60,
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def implementation(self, i = {}):
        display_name = i.get('display_name')
        interval = i.get('interval')
        service_class_name = i.get('class')

        service_class = Service.find(service_class_name)

        assert service_class != None, "invalid service"

        new_service = ServiceInstance()
        new_service.service_name = service_class.getName()
        new_service.display_name = display_name
        new_service.data = "{}"

        if interval != None:
            new_service.interval = interval

        new_service.save()

        return new_service.getStructure()
