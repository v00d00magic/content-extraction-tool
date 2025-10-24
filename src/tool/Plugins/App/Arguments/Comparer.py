from Objects.Object import Object
from Plugins.Data.NameDictList import NameDictList
from .ArgumentDict import ArgumentDict
from .Argument import Argument
from pydantic import Field
from App import app

class Comparer(Object):
    compare: NameDictList = Field(default=None)
    values: dict | ArgumentDict = Field(default={})
    raise_on_assertions: bool = Field(default=False)
    missing_args_inclusion: bool = Field(default=False)
    default_on_none: bool = Field(default=True)
    default_on_assertion: bool = Field(default=True)
    none_values_skipping: bool = Field(default=True)

    def toDict(self) -> ArgumentDict:
        if self.compare == None:
            return self.values

        table = ArgumentDict()
        names = []
        if getattr(self.values, "toNames", None) != None:
            names = self.values.toNames()
        else:
            for name, val in self.values.items():
                names.append(name)

        for name in self.compare.toNames():
            names.append(name)

        for param_name in names:
            try:
                app.Logger.log(f"getting name={param_name}", section=["Comparer"])
            except:
                pass

            got_value = self.byName(param_name, missing_args_inclusion = self.missing_args_inclusion)
            if got_value == None and self.none_values_skipping == True:
                continue

            table.add(param_name, got_value)

        return table

    def byName(self, name, check_assertions: bool = True, missing_args_inclusion: bool = False):
        inputs = self.values.get(name)
        argument: Argument = self.compare.get(name)

        if argument == None:
            if missing_args_inclusion == True:
                return inputs
            else:
                return None

        argument.setInput(inputs)
        fallback = argument.sensitive_default

        value = argument.getValue()

        if value == None and self.default_on_none == True:
            value = fallback

        try:
            app.Logger.log(f"{name}={inputs}={str(value)}", section=["Comparer"])
        except:
            pass

        if check_assertions == True:
            try:
                argument.current = value
                argument.checkAssertions()
            except Exception as assertion:
                try:
                    app.Logger.log(assertion, "Executables!Declaration")
                except:
                    print(assertion)

                if self.raise_on_assertions == True:
                    raise assertion

                if self.default_on_assertion == True:
                    argument.current = fallback

        return value

    def diff(self):
        diff_value = 0

        for item_name in self.compare.toNames():
            if self.values.get(item_name) != None:
                #diff_value += 1
                return True

        return False
