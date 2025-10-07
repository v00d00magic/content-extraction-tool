from Plugins.Arguments.Argument import Argument

class StringArgument(Argument):
    def implementation(self):
        if self.current == None:
            return None

        return str(self.current)
