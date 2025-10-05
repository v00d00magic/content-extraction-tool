from pathlib import Path
from Objects.Object import Object
from Objects.Configurable import Configurable
from Plugins.Arguments.Comparer import Comparer
from Plugins.Arguments.ArgumentList import ArgumentList
from Objects.classproperty import classproperty
from pydantic import Field, computed_field
import json

class Config(Object, Configurable):
    path: Path = Field()
    name: str = Field(default="config.json")
    comparer: Comparer = Comparer(
        raise_on_assertions = False,
        default_on_none = True
    )

    @computed_field
    @property
    def file(self) -> Path:
        return self.path.joinpath(self.name)

    def __del__(self):
        try:
            self._stream.close()
        except AttributeError:
            pass

    @classproperty
    def options(cls) -> ArgumentList:
        from Plugins.Arguments.Types.BooleanArgument import BooleanArgument

        return ArgumentList([
            BooleanArgument(
                name = "config.external_editing.allow",
                default = True
            )
        ])

    def get(self, option: str, default: str = None):
        got = self.comparer.byName(option)
        if got == None:
            return default

        return got

    def set(self, option: str, value: str):
        if value == None:
            del self.comparer.values[option]
        else:
            self.comparer.values[option] = value

        self.updateFile()

    def checkFile(self):
        self.path.mkdir(parents=True,exist_ok=True)
        if self.file.exists() == False:
            t = open(self.file, 'w', encoding='utf-8')
            json.dump({}, t)
            t.close()

        self._stream = open(self.file, 'r+', encoding='utf-8')
        try:
            self.comparer.values = json.load(self._stream)
        except json.JSONDecodeError as __exc:
            self._stream.write("{}")

    def updateFile(self):
        self._stream.seek(0)

        json.dump(self.comparer.dict(), self._stream, indent=4)

        self._stream.truncate()

    def reset(self):
        self._stream.seek(0)
        self._stream.write("{}")
        self._stream.truncate()

        self.comparer.values = {}

    def isItemHidden(self, name):
        for item in self.hidden_items:
            return item.startswith(name)
