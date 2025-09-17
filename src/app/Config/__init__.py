from app.Config.DefaultSettings import DefaultSettings
from pathlib import Path
import json

class Config():
    '''
    param->value comparer
    Allows to recieve value by option name
    Stores in %storage%/settings
    '''

    def __init__(self, cwd, file_name: str = 'config.json', fallback = DefaultSettings):
        '''
        file_name: name of the file
        fallback: params to compare
        '''

        self.compared_options = fallback
        self.path = Path(f"{str(cwd)}/storage/settings/{file_name}")

        self.__load_path(self.path)
        self.__pass_declarable()

        # hardcode oh yeah
        if file_name == "config.json":
            self.hidden_items = ["db.", "web."]
            self.is_hidden = True

    def __pass_declarable(self):
        from declarable.ArgsComparer import ArgsComparer

        self.declared_settings = ArgsComparer(compare=self.compared_options, 
                                              args=self.passed_options, 
                                              exc="pass", 
                                              default_sub=True,
                                              same_dict_mode=self.compared_options == None)
        self.options = self.declared_settings.dict()

    def __load_path(self, path):
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

    def __update_file(self):
        self.config_stream.seek(0)

        json.dump(self.passed_options, self.config_stream, indent=4)

        self.config_stream.truncate()

    def get(self, option: str, default: str = None):
        '''
        Recieves option value by name.

        Params:

        option: name of the option

        default: value that will be returned if param value is \"None\"
        '''

        return self.options.get(option, default)

    def set(self, option: str, value: str):
        '''
        Sets option in config file.

        Params:

        option: option name

        value: value that will be set
        '''

        if value == None:
            del self.passed_options[option]
        else:
            self.passed_options[option] = value

        self.__update_file()
        self.__pass_declarable()

    def reset(self):
        '''
        Clears config file.
        '''

        self.config_stream.seek(0)
        self.config_stream.write("{}")
        self.config_stream.truncate()

        self.options = {}
