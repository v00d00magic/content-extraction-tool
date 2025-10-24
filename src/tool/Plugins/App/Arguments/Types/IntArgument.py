from ...Arguments.Argument import Argument

class IntArgument(Argument):
    def implementation(self, i = {}):
        if self.inputs == None:
            return None

        return int(self.inputs)
