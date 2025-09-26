import json
from Utils.Util import Util

class JSON(Util):
    def parse(self):
        if type(self.data) == str:
            return json.loads(self.data)

        return self.data

    def dump(self, indent = None):
        return json.dumps(self.data, ensure_ascii = False, indent = indent)

    def isValid(self):
        try:
            val = self.data

            return val != None and type(val) != int and type(val) != str
        except json.JSONDecodeError:
            return False
        except TypeError:
            return False
