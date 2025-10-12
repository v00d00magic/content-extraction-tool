from Objects.Object import Object
from Objects.Namespace import Namespace
from .Templates import Meta, Execute, Saver, Variables, EnvVariables
from typing import Any
from pydantic import Field

class Executable(Object, Namespace):
    self_name: str = "None"
    call: Any = Field(default = None)
    meta: Any = None
    variables: Any = None
    env_variables: Any = None
    execute: Any = None
    saver: Any = None

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

    def init_subclass(self):
        self.meta = self.Meta(self)
        self.variables = self.Variables(self)
        self.env_variables = self.EnvVariables(self)

    def constructor(self):
        self.execute = self.Execute(self)
        self.saver = self.Saver(self)
