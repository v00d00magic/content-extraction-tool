from Declarable.Arguments.ArgsDict import ArgsDict
from App import app

class ArgsComparer():
    EXCEPT_PASS = "pass"
    EXCEPT_ASSERT = "assert"

    DEFAULT_ON_NONE = True

    def __init__(self, 
                 compare: dict, 
                 args: dict, 
                 exc: str = "assert", 
                 default_sub = True,
                 missing_args_inclusion: bool = False, 
                 same_dict_mode: bool = False):
        self.compare = compare # Argument class dict
        self.args = args # what we got at input
        self.exc = exc
        self.missing_args_inclusion = missing_args_inclusion # Return the same value if argument didnt found in compared
        self.same_dict_mode = same_dict_mode # Return input dict
        self.default_sub = default_sub # Pass default value insted of None if None
        self.save_none_values = False # Save dict key even if None

    def diff(self):
        self.missing_args_inclusion = False
        self.default_sub = False
        diff_value = 0

        for item_name, item_content in self.compare.items():
            if self.args.get(item_name) != None:
                diff_value += 1

        return diff_value > 0

    def dict(self):
        if self.same_dict_mode == True:
            return self.args

        table = ArgsDict()

        options = {}
        if getattr(self.args, "__dict__", None) != None:
            options = self.args.__dict__()
        else:
            options = dict(self.args)

        options.update(self.compare)

        for param_name, param_item in options.items():
            try:
                app.logger.log(f"ArgsComparer: getting name={param_name}", section=["Executables", "Declaration", "Name"])
            except:
                pass

            got_value = self.getByName(param_name)
            if got_value == None and self.save_none_values == False:
                continue

            table.add(param_name, got_value)

        return table

    def getByName(self, name, check_assertions = True):
        inputs_value = self.args.get(name)
        argument = self.compare.get(name)

        if argument == None:
            if self.missing_args_inclusion == True:
                return inputs_value
            else:
                return None

        fallback = argument.getSensitiveDefault()

        argument.data['name'] = name
        argument.passValue(inputs_value)

        value = argument.getResult(self.default_sub)

        try:
            app.logger.log(f"ArgsComparer: {name}={inputs_value}={str(value)}", section=["Executables", "Declaration", "Name"])
        except:
            pass

        if check_assertions == True:
            try:
                argument.assertions()
            except Exception as assertion:
                try:
                    app.logger.log(assertion, "Executables!Declaration")
                except:
                    print(assertion)

                if self.exc == ArgsComparer.EXCEPT_ASSERT:
                    raise assertion
                else:
                    if self.default_sub == True:
                        value = fallback

        return value
