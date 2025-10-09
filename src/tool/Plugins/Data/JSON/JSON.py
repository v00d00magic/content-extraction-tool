from Plugins.Executables.Types.Representation import Representation
import json

class JSON(Representation):
    def parse(self, data):
        if type(data) == str:
            return json.loads(data)

        return data

    def dump(self, data, indent = None):
        return json.dumps(data, ensure_ascii = False, indent = indent)

    def isValid(self, data):
        try:
            return data != None and type(data) != int and type(data) != str
        except json.JSONDecodeError:
            return False
        except TypeError:
            return False
