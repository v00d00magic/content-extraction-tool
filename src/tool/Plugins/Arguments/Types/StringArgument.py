from Plugins.Arguments.Argument import Argument

class StringArgument(Argument):
    def implementation(self):
        return str(self.current)
