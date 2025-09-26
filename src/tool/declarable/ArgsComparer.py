from declarable.ArgsDict import ArgsDict
from app.App import logger

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
            got_value = self.getByName(param_name)
            if got_value == None and self.save_none_values == False:
                continue

            table.add(param_name, got_value)

        return table

    def getByName(self, name, check_assertions = True):
        inputs_value = self.args.get(name)
        param_object = self.compare.get(name)

        if param_object == None:
            if self.missing_args_inclusion == True:
                return inputs_value
            else:
                return None

        fallback = param_object.default()
        set_default = self.default_sub

        param_object.configuration['name'] = name
        param_object.input_value(inputs_value)

        value = param_object.getResult(set_default)

        logger.log(f"ArgsComparer: {name}={str(value)}", section=["Executables", "Declaration", "Name"])

        if check_assertions == True:
            try:
                param_object.assertions()
            except Exception as assertion:
                try:
                    from app.App import logger

                    logger.log(assertion, "Executables!Declaration")
                except:
                    print(assertion)

                if self.exc == ArgsComparer.EXCEPT_ASSERT:
                    raise assertion
                else:
                    if set_default == True:
                        value = fallback

        return value
