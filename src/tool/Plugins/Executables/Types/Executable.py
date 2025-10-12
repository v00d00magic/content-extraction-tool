from Objects.Object import Object
from Objects.Namespace import Namespace
from .Templates import Meta, Execute, Saver, Variables, EnvVariables
from typing import Any
from pydantic import Field

class Executable(Object, Namespace):
    self_name: str = "None"
    call: Any = Field(default = None)
    meta: Any = Field(default = None)
    execute: Any = Field(default = None)
    saver: Any = Field(default = None)

    class Meta(Meta.Meta):
        pass

    class Execute(Execute.Execute):
        pass

    class Saver(Saver.Saver):
        pass

    class Variables(Variables.Variables):
        pass

    class EnvVariables(EnvVariables.EnvVariables):
        pass

    def init_subclass(cls):
        cls.meta = cls.Meta(cls)
        cls.variables = cls.Variables(cls)
        cls.env_variables = cls.EnvVariables(cls)

    def constructor(self):
        self.execute = self.Execute(self)
        self.saver = self.Saver(self)
