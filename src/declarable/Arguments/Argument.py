from resources.Exceptions import InvalidArgumentName
from resources.Consts import consts

class Argument:
    cache_results = True

    def __init__(self, configuration):
        if configuration.get('name') in consts.get('arguments.forbidden'):
            raise InvalidArgumentName(f"{configuration.get('name')} is invalid argument name")

        self.configuration = configuration

    # logic violation
    def input_value(self, val):
        self.passed_value = val

    # This method must be changed in inherited!
    def value(self):
        return self.passed_value

    def default(self):
        if self.configuration.get("env") != None:
            from app.App import env

            env_arg = self.configuration.get("env")

            return env.get(env_arg.get("name"), env_arg.default())

        return self.configuration.get('default', None)

    def sensitive_default(self):
        if self.configuration.get('sensitive') == True:
            return None
        else:
            return self.default()

    def get(self, name, default = None):
        return self.configuration.get(name, default)

    def manual(self):
        return self.configuration.get("docs")

    def getStructure(self):
        payload = self.configuration.copy()
        payload.update({
            'type': self.__class__.__name__,
            'docs': self.manual()
        })

        payload['default'] = self.sensitive_default()

        return payload

    def val(self, default_sub = True):
        if self.cache_results == True:
            if getattr(self, "recieved_value", None) != None:
                return self.recieved_value

        got = None
        if self.passed_value != None:
            try:
                got = self.value()
            except Exception as e:
                if default_sub == True:
                    got = self.default()
        else:
            if default_sub == True:
                got = self.default()

        self.recieved_value = got

        return got

    def assertions(self):
        assertions_list = self.configuration.get("assertion")

        if assertions_list != None:
            for assertion_name, assertion_item in assertions_list.items():
                _method = getattr(self, "assertion_" + assertion_name, None)
                if _method != None:
                    _method(assertion_item)

    def assertion_not_null(self, item):
        this_name = self.configuration.get('name')
        assert self.recieved_value != None, f"{this_name} is null"

    def _assertion_only_when(self, item):
        for condition in item:
            _en = list(enumerate(condition))
            key_name = _en[0][1]
            key_value = condition.get(key_name)

            operator = key_value.get("operator")

            match(operator):
                case "==":
                    assert self.all_args.get(key_name) == key_value.get("value"), f"{key_name} caused assertion"
                case "!=":
                    assert self.all_args.get(key_name) != key_value.get("value"), f"{key_name} caused assertion"
