from Objects.Object import Object
from Plugins.Data.NameDictList import NameDictList
from Plugins.Arguments.ArgumentDict import ArgumentDict
from pydantic import Field
from App import app

class Comparer(Object):
    compare: NameDictList = Field(default=None)
    values: dict | ArgumentDict = Field(default={})
    raise_on_assertions: bool = Field(default=False)
    missing_args_inclusion: bool = Field(default=False)
    default_on_none: bool = Field(default=True)
    none_values_skipping: bool = Field(default=True)

    def toDict(self) -> ArgumentDict:
        if self.compare == None:
            return self.values

        table = ArgumentDict()
        names = []
        if getattr(self.values, "toDict", None) != None:
            names = self.values.toDict()
        else:
            for name, val in self.values.items():
                names.append(name)

        for name in self.compare.toNames():
            names.append(name)

        for param_name in names:
            try:
                app.logger.log(f"ArgsComparer: getting name={param_name}", section=["Comparer"])
            except:
                pass

            got_value = self.byName(param_name)
            if got_value == None and self.none_values_skipping == True:
                continue

            table.add(param_name, got_value)

        return table

    def byName(self, name, check_assertions = True):
        inputs = self.values.get(name)
        argument = self.compare.get(name)

        if argument == None:
            if self.missing_args_inclusion == True:
                return inputs
            else:
                return None

        argument.setInput(inputs)
        fallback = argument.sensitive_default

        value = argument.getValue()

        if value == None and self.default_on_none == True:
            value = fallback

        try:
            app.logger.log(f"ArgsComparer: {name}={inputs}={str(value)}", section=["Comparer"])
        except:
            pass

        if check_assertions == True:
            try:
                argument.current = value
                argument.checkAssertions()
            except Exception as assertion:
                try:
                    app.logger.log(assertion, "Executables!Declaration")
                except:
                    print(assertion)

                if self.raise_on_assertions == True:
                    raise assertion

        return value

    def diff(self):
        self.missing_args_inclusion = False
        self.default_sub = False
        diff_value = 0

        for item_name, item_content in self.compare.items():
            if self.args.get(item_name) != None:
                diff_value += 1

        return diff_value > 0
