from Objects.classproperty import classproperty

class Submodulable():
    @classmethod
    def getInheritFrom(cls):
        return ["self"]

    # submodules = []

    def __init_subclass__(cls, **kwargs):
        cls.submodules = []

        return super().__init_subclass__(**kwargs)

    @classproperty
    def receivations(cls):
        return cls.getSubmodulesByType("Receivation")

    @classproperty
    def external_extractors(cls):
        return cls.getSubmodulesByType("ExternalExtractor")

    @classproperty
    def acts(cls):
        return cls.getSubmodulesByType("Act")

    @classproperty
    def confirmations(cls):
        return cls.getSubmodulesByType("Confirmation")

    @classmethod
    def getSubmodulesByType(cls, type=None):
        _items = []

        for inherit_item in cls.getInheritFrom():
            if inherit_item == "self":
                inherit_item = cls

            for sub in inherit_item.submodules:
                if type == None:
                    _items.append(sub)
                else:
                    if sub.self_name == type:
                        _items.append(sub)

        return _items

    @classmethod
    def addSubmodule(cls, submodule):
        cls.submodules.append(submodule)

    def setOuter(self, outer):
        self.outer = outer

    @classmethod
    def _build_submodules(cls):
        from ..Types.Extractor import Extractor
        from ..Types.Act import Act

        class AbstractAct(Act):
            self_name = "Act"
            section_name = ["Act", cls.getName()]
            outer = cls

        class AbstractReceivation(Extractor):
            self_name = "Receivation"
            section_name = ["Receivation", cls.getName()]
            outer = cls

            def selfInsert(self, item):
                item.SavedVia.sign(self, self.outer)

        class AbstractExternalExtractor(Extractor):
            self_name = "ExternalExtractor"
            section_name = ["ExternalExtractor", cls.getName()]
            outer = cls

            def selfInsert(self, item):
                item.SavedVia.sign(self, self.outer)

        class AbstractConfirmation(Extractor):
            self_name = "Confirmation"
            section_name = ["Confirmation", cls.getName()]
            outer = cls

        cls.AbstractAct = AbstractAct
        cls.AbstractReceivation = AbstractReceivation
        cls.AbstractExternalExtractor = AbstractExternalExtractor
        cls.AbstractConfirmation = AbstractConfirmation
