from Objects.Object import Object
from Plugins.Arguments.ArgumentList import ArgumentList
from Plugins.Arguments.ArgumentDict import ArgumentDict
from pydantic import Field
from App import app

class Comparer(Object):
    compare: ArgumentDict = Field(default=None)
    values: dict = Field(default={})
    raise_on_assertions: bool = Field(default=False)
    missing_args_inclusion: bool = Field(default=False)
    default_on_none: bool = Field(default=True)
    none_values_skipping: bool = Field(default=True)

    def toDict(self):
        if self.compare == None:
            return self.values

        table = ArgumentDict()
        iteration_options = {}
        if getattr(self.args, "__dict__", None) != None:
            iteration_options = self.args.__dict__()
        else:
            iteration_options = dict(self.args)

        iteration_options.update(self.compare)

        for param_name, param_item in iteration_options.items():
            try:
                app.logger.log(f"ArgsComparer: getting name={param_name}", section=["Comparer"])
            except:
                pass

            got_value = self.byName(param_name)
            if got_value == None and self.none_values_skipping == True:
                continue

            table.add(param_name, got_value)

        return

    def byName(self, name, check_assertions = True):
        inputs = self.values.get(name)
        argument = self.compare.get(name)

        if argument == None:
            if self.missing_args_inclusion == True:
                return inputs
            else:
                return None

        argument.current = inputs
        fallback = argument.sensitive_default

        value = argument.value()
        if value == None and self.default_on_none == True:
            value = argument.default

        try:
            app.logger.log(f"ArgsComparer: {name}={inputs}={str(value)}", section=["Comparer"])
        except:
            pass

        if check_assertions == True:
            try:
                argument.checkAssertions()
            except Exception as assertion:
                try:
                    app.logger.log(assertion, "Executables!Declaration")
                except:
                    print(assertion)

                if self.raise_on_assertions == True:
                    raise assertion
                else:
                    if self.default_on_none == True:
                        value = fallback

        return value

    def diff(self):
        self.missing_args_inclusion = False
        self.default_sub = False
        diff_value = 0

        for item_name, item_content in self.compare.items():
            if self.args.get(item_name) != None:
                diff_value += 1

        return diff_value > 0
