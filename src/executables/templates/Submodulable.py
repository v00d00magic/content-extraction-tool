from utils.ClassProperty import classproperty

class Submodulable():
    inherit_from = ["self"]
    # submodules = []

    def __init_subclass__(cls, **kwargs):
        cls.submodules = []

        return super().__init_subclass__(**kwargs)

    @classproperty
    def extractors(cls):
        return cls.get_submodules_by_type("Extractor")

    @classmethod
    def get_submodules_by_type(cls, type):
        _items = []

        for inherit_item in cls.inherit_from:
            if inherit_item == "self":
                inherit_item = cls

            for sub in inherit_item.submodules:
                if sub.self_name == type:
                    _items.append(sub)

        return _items

    @classmethod
    def add_submodule(cls, submodule):
        cls.submodules.append(submodule)
