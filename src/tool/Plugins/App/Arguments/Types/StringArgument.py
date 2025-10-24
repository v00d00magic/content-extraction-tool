from ..Argument import Argument

class StringArgument(Argument):
    def implementation(self, i = {}):
        if self.inputs == None:
            return None

        return str(self.inputs)
