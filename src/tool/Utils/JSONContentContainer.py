from App.Logger.LogKind import LogKind
from App import app
from Utils.Data.JSON import JSON
import json

class JSONContentContainer():
    _cached = None

    @classmethod
    def get_description(cls):
        return cls.__name__

    @classmethod
    def get_attr(cls):
        pass

    @classmethod
    def attr_json(cls, new_data):
        return JSON(new_data).dump()

    @classmethod
    def set_attr(cls, new_data):
        pass

    @classmethod
    def get_cached(cls):
        return cls._cached

    @classmethod
    def getData(cls):
        app.logger.log(f"Getting {cls.get_description()} property",section=["Saveable", "Container"])

        if cls.get_cached() != None:
            return cls.get_cached()

        if cls.get_attr() == None:
            return {}

        try:
            cls._cached = JSON(cls.get_attr()).parse()
        except json.decoder.JSONDecodeError:
            app.logger.log(f"Container {cls.get_description()} contains wrong json", kind = LogKind.KIND_ERROR, section = ["Saveable", "Container"])
            return None

        return cls._cached

    @classmethod
    def update(cls, new_data):
        _data = cls.getData()
        _data.update(new_data)

        app.logger.log(f"Updated container {cls.get_description()}",section=["Saveable", "Container"])

        cls.set_attr(_data)

    @classmethod
    def get(cls, key, default = None):
        return cls.getData().get(key, default)
