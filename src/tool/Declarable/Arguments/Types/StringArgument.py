from Declarable.Arguments.Argument import Argument
from Utils.Data.Text import Text

class StringArgument(Argument):
    def get_maxlength(self):
        return self.data.get('maxlength', None)

    def implementation(self)->str:
        inp = str(self.passed_value)
        if len(inp) == 0:
            if self.data.get('return_none_on_empty', True) == True:
                return self.getDefault()

        if self.get_maxlength() != None:
            return Text(inp).cut(int(self.data.get("maxlength")), multipoint=False)
        else:
            return inp
