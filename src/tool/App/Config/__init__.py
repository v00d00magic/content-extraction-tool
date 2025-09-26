from App.Config.DefaultSettings import DefaultSettings
from pathlib import Path
import json

class Config():
    def __init__(self, cwd, file_name: str = 'config.json', fallback = DefaultSettings):
        self.compared_options = fallback

        Path(cwd).joinpath("storage").joinpath("config").mkdir(parents=True,exist_ok=True)

        self.path = Path(f"{str(cwd)}/storage/config/{file_name}")

        self.loadPath(self.path)
        self.passDeclarable()

    def setAsConf(self):
        self.hidden_items = ["db.", "web."]
        self.is_hidden = True

    def passDeclarable(self):
        from Declarable.Arguments.ArgsComparer import ArgsComparer

        self.declared_settings = ArgsComparer(compare=self.compared_options, 
                                              args=self.passed_options, 
                                              exc=ArgsComparer.EXCEPT_PASS, 
                                              default_sub=True,
                                              same_dict_mode=self.compared_options == None)
        self.options = self.declared_settings.dict()

    def loadPath(self, path: Path):
        if path.exists() == False:
            __temp_config_write_stream = open(self.path, 'w', encoding='utf-8')
            json.dump({}, __temp_config_write_stream)
            __temp_config_write_stream.close()

        self.config_stream = open(str(path), 'r+', encoding='utf-8')
        try:
            self.passed_options = json.load(self.config_stream)
        except json.JSONDecodeError as __exc:
            self.config_stream.write("{}")
            self.passed_options = dict()

    def __del__(self):
        try:
            self.config_stream.close()
        except AttributeError:
            pass

    def updateFile(self):
        self.config_stream.seek(0)

        json.dump(self.passed_options, self.config_stream, indent=4)

        self.config_stream.truncate()

    def get(self, option: str, default: str = None):
        got = self.declared_settings.getByName(option)
        if got == None:
            return default

        return got

    def set(self, option: str, value: str):
        if value == None:
            del self.passed_options[option]
        else:
            self.passed_options[option] = value

        self.updateFile()
        self.passDeclarable()

    def reset(self):
        self.config_stream.seek(0)
        self.config_stream.write("{}")
        self.config_stream.truncate()

        self.options = {}
