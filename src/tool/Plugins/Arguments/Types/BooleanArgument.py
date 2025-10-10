from Plugins.Arguments.Argument import Argument

class BooleanArgument(Argument):
    def implementation(self, i = {}):
        return int(self.inputs) == 1
