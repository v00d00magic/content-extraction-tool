from utils.ClassProperty import classproperty

class Submodulable():
    inherit_from = ["self"]
    # submodules = []

    def __init_subclass__(cls, **kwargs):
        cls.submodules = []

        return super().__init_subclass__(**kwargs)

    @classproperty
    def receivations(cls):
        return cls.get_submodules_by_type("Receivation")

    @classproperty
    def external_extractors(cls):
        return cls.get_submodules_by_type("ExternalExtractor")

    @classproperty
    def acts(cls):
        return cls.get_submodules_by_type("Act")

    @classproperty
    def confirmations(cls):
        return cls.get_submodules_by_type("Confirmation")

    @classmethod
    def get_submodules_by_type(cls, type=None):
        _items = []

        for inherit_item in cls.inherit_from:
            if inherit_item == "self":
                inherit_item = cls

            for sub in inherit_item.submodules:
                if type != None and sub.self_name == type:
                    _items.append(sub)

        return _items

    @classmethod
    def add_submodule(cls, submodule):
        cls.submodules.append(submodule)

    @classmethod
    def _build_submodules(cls):
        from executables.templates.extractors import Extractor
        from executables.templates.acts import Act

        class AbstractAct(Act):
            self_name = "Act"
            section_name = "Act!" + cls.full_name()
            outer = cls

        class AbstractReceivation(Extractor):
            self_name = "Receivation"
            section_name = "Receivation!" + cls.full_name()
            outer = cls

            @classmethod
            def selfInsert(cls, item):
                item.markSavedJson(cls)

        class AbstractExternalExtractor(Extractor):
            self_name = "ExternalExtractor"
            section_name = "ExternalExtractor!" + cls.full_name()
            outer = cls

            @classmethod
            def selfInsert(cls, item):
                item.markSavedJson(cls)

        class AbstractConfirmation(Extractor):
            self_name = "Confirmation"
            section_name = "Confirmation!" + cls.full_name()
            outer = cls

        cls.AbstractAct = AbstractAct
        cls.AbstractReceivation = AbstractReceivation
        cls.AbstractExternalExtractor = AbstractExternalExtractor
        cls.AbstractConfirmation = AbstractConfirmation
