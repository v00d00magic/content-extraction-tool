from Objects.Executables.Types.Representation import Representation
import json

locale_keys = {
    "json.name": {
        "en_US": "JSON"
    }
}

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

    @classmethod
    def defineMeta(cls):
        return {
            'name': cls.key("json.name")
        }
