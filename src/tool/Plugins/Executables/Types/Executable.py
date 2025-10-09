from Objects.Object import Object
from Objects.Namespace import Namespace
from .Templates import Arguments, Meta, Execute, Saver, Variables, EnvVariables

class Executable(Object, Namespace):
    self_name: str = "None"

    class Arguments(Arguments.Arguments):
        pass

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

    def __init_subclass__(self):
        self.arguments = self.Arguments(self)
        self.meta = self.Meta(self)
        self.execute = self.Execute(self)
        self.saver = self.Saver(self)
        self.variables = self.Variables(self)
        self.env_variables = self.EnvVariables(self)

    # you can use __init__ as you want
