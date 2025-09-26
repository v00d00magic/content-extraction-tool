from executables.list.Data.Json import Implementation as Json

class Implementation(Json):
    section = "RSS"

    @classmethod
    def getInheritFrom(cls):
        return [Json]
