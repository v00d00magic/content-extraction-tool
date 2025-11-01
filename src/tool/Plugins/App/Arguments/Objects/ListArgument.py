from ...Arguments.Argument import Argument
from pydantic import Field, computed_field

class ListArgument(Argument):
    orig: Argument = Field(default = None)
    total_count: int = Field(default=0)

    def implementation(self, i = {}):
        results: list = []
        value: list = self.inputs

        # WORKAROUND

        try:
            from Plugins.Data.JSON import JSON

            if type(value) == str:
                _json = JSON(value)
                if _json.isValid() == True:
                    value = _json.getSelf()
        except:
            pass

        if self.orig == None:
            return value

        for item in value:
            _orig = self.orig
            _orig.setInput(item)

            results.append(_orig.getValue())

        return results

    def getCount(self):
        return len(self.current)

    def getCompleteness(self):
        return self.getCount() / self.total_count

    def append(self, item):
        self.current.append(item)
