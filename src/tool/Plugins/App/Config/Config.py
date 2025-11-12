from pathlib import Path
from Objects.Object import Object
from Objects.Configurable import Configurable
from Plugins.App.Arguments.Comparer import Comparer
from Plugins.Data.NameDictList import NameDictList
from Objects.ClassProperty import classproperty
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

    @staticmethod
    def mount():
        from App import app

        configs = Config(
            path = app.cwd.parent.joinpath("storage").joinpath("config")
        )
        # dont like it but well
        configs.checkFile()
        configs.updateCompare()
        app.mount('Config', configs)

    def updateCompare(self):
        '''
        WORKAROUND. updates settings from app globals
        '''
        from App import app

        self.comparer.compare = NameDictList.fromDict(app.settings)

    def __del__(self):
        try:
            self._stream.close()
        except AttributeError:
            pass

    @classproperty
    def options(cls) -> NameDictList:
        from Plugins.App.Arguments.Types.BooleanArgument import BooleanArgument

        return NameDictList([
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
            temp_stream = open(self.file, 'w', encoding='utf-8')
            default_settings = dict()

            '''for item in self.comparer.compare.toList():
                _default = item.default

                def _model_dump(_item):
                    if hasattr(_item, 'model_dump') == True:
                        return _item.model_dump()
                    else:
                        return _item.default

                if type(_default) == list:
                    default_settings[item.name] = []
                    for val in _default:
                        default_settings.get(item.name).append(_model_dump(item))
                else:
                    default_settings[item.name] = _model_dump(item)'''

            json.dump(default_settings, temp_stream)
            temp_stream.close()

        self._stream = open(self.file, 'r+', encoding='utf-8')
        try:
            self.comparer.values = json.load(self._stream)
        except json.JSONDecodeError as __exc:
            self._stream.write("{}")

    def updateFile(self) -> None:
        self._stream.seek(0)

        json.dump(self.comparer.dict(), self._stream, indent=4)

        self._stream.truncate()

    def reset(self) -> None:
        '''
        Clears all the settings
        '''
        self._stream.seek(0)
        self._stream.write("{}")
        self._stream.truncate()

        self.comparer.values = {}
