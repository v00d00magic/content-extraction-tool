from Plugins.Arguments.Argument import Argument

class StringArgument(Argument):
    def implementation(self):
        if self.value == None:
            return None

        return str(self.value)
