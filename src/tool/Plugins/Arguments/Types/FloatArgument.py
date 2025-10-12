from Plugins.Arguments.Argument import Argument

class FloatArgument(Argument):
    def implementation(self, i = {}):
        if self.inputs == None:
            return None

        return float(self.inputs)
