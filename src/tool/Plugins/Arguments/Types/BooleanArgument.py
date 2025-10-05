from Plugins.Arguments.Argument import Argument

class BooleanArgument(Argument):
    def implementation(self):
        return int(self.current) == 1
