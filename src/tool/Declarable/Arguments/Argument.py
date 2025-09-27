from App import app

class InvalidArgumentName(Exception):
    pass

class Argument:
    forbidden = ["i", "name", "confirm"]

    def __init__(self, data):
        assert data.get('name') not in self.forbidden

        self.data = data
        self.passed_value = None
        self.value = None

    def getDefault(self):
        if self.data.get("env") != None:
            env_arg = self.data.get("env")

            return app.env.get(env_arg.get("name"), env_arg.getDefault())

        return self.data.get('default', None)

    def getSensitiveDefault(self):
        if self.data.get('sensitive') == True:
            return None
        else:
            return self.getDefault()

    def get(self, name, default = None):
        return self.data.get(name, default)

    def getDocs(self):
        return self.data.get("docs")

    def getStructure(self):
        payload = self.data.copy()
        payload["type"] = self.__class__.__name__

        defaults = self.getSensitiveDefault()

        if payload.get("class") != None:
            payload["class"] = payload.get("class").getStructure()

        if type(defaults) == list:
            i = 0
            for default in defaults:
                if hasattr(default, "toJson") == True:
                    defaults[i] = default.toJson()

                i+=1
        
        payload['default'] = defaults

        return payload

    def getResult(self, default_instead_none = True):
        got = None
        if self.passed_value != None:
            try:
                got = self.implementation()
            except Exception as e:
                try:
                    app.logger.log(e, "Executables!Declaration")
                except:
                    print(e)

                if default_instead_none == True:
                    got = self.getDefault()
        else:
            if default_instead_none == True:
                got = self.getDefault()

        self.value = got

        return self.value

    def passValue(self, val):
        self.passed_value = val

    def implementation(self):
        return self.passed_value

    def assertions(self):
        assertions_list = self.data.get("assertion")

        if assertions_list != None:
            for assertion_name, assertion_item in assertions_list.items():
                assertion_method = getattr(self, "assertion_" + assertion_name, None)
                if assertion_method != None:
                    assertion_method(assertion_item)

    def assertion_not_null(self, item):
        this_name = self.data.get('name')
        assert self.value != None, f"{this_name} is null"

    def _assertion_only_when(self, item):
        for condition in item:
            dicts = condition.items()
            key_name = dicts[0]
            key_value = condition.get(key_name)

            operator = key_value.get("operator")

            match(operator):
                case "==":
                    assert self.all_args.get(key_name) == key_value.get("value"), f"{key_name} caused assertion"
                case "!=":
                    assert self.all_args.get(key_name) != key_value.get("value"), f"{key_name} caused assertion"
