from Executables.templates.acts import Act
from Declarable.Arguments import ServiceInstanceArgument, JsonArgument

class Implementation(Act):
    @classmethod
    def declare(cls):
        params = {}
        params["service"] = ServiceInstanceArgument({
            "assertion": {
                "not_null": True,
            }
        })
        params["data"] = JsonArgument({
            "assertion": {
                "not_null": True,
            }
        })

        return params

    async def implementation(self, i = {}):
        service = i.get('service')
        data = i.get('data')

        service.updateData(data)
        service.save()

        return True
