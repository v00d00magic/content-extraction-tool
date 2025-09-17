from executables.templates.services import Service
from executables.templates.acts import Act
from executables.templates.extractors import Extractor
from app.App import logger
from declarable.Arguments import LimitedArgument, StringArgument, ObjectArgument

class FatalError(Exception):
    pass

class Implementation(Service):
    c_cached_executable = None
    pass_args = {}

    @classmethod
    def declare(cls):
        params = {}
        params["executable_type"] = LimitedArgument({
            "values": ["act", "extractor"],
            "assertion": {
                "not_null": True,
            },
        })
        params["executable_name"] = StringArgument({
            "assertion": {
                "not_null": True,
            },
        })
        params["pass_args"] = ObjectArgument({
            "default": {},
            "assertion": {
                "not_null": True,
            },
        })

        return params

    def __get_executable(self, executable_name, executable_type):
        self.pass_args = self.config.get("pass_args", {})
        if self.c_cached_executable == None:
            match(executable_type):
                case "act":
                    self.c_cached_executable = Act.find(executable_name)
                case "extractor":
                    self.c_cached_executable = Extractor.find(executable_name)

        if self.c_cached_executable == None:
            raise FatalError("executable not found")

    async def implementation(self, i = {}):
        executable_type = self.config.get("executable_type")
        executable_name = self.config.get("executable_name")

        if executable_type == None:
            raise FatalError("executable_type is not passed in \"data\"")

        self.__get_executable(executable_name, executable_type)

        logger.log(message=f"Called {executable_name}", kind="message", section=logger.SECTION_SERVICES)

        __exec = self.c_cached_executable()

        res = await __exec.execute_with_validation(args=self.pass_args)
        if executable_type == "act":
            print(res)
