from resources.Exceptions import AbstractClassException, SuitableExtractMethodNotFound
from thumbnails import ThumbnailMethod
from declarable.ArgsComparer import ArgsComparer
from executables.templates.extractors import Extractor
from executables.templates.acts import Act
from executables.templates.Executable import Executable

class RepresentationMeta(type):
    def __init__(cls, name, bases, attrs):
        if not name.startswith('_') and bases != (object,):
            cls._build_submodules()
        super().__init__(name, bases, attrs)

class Representation(Executable, metaclass=RepresentationMeta):
    self_name = "Representation"

    @classmethod
    def declare_recursive(cls):
        _extractors_args = cls.sum_arguments(cls.receivations)

        _fnl = _extractors_args
        _fnl.update(super().declare_recursive())

        return _fnl

    @classmethod
    def sum_arguments(cls, extractors):
        _sum = {}
        for extractor_item in extractors:
            rec = extractor_item.declare_recursive()
            for name, item in rec.items():
                _sum[name] = item

        return _sum

    @classmethod
    def divide_arguments(cls, extractors):
        _sum = {}
        for extractor_item in extractors:
            _sum[extractor_item.full_name()] = extractor_item.declare_recursive()

        return _sum

    @classmethod
    def find_suitable_extractor(cls, args):
        if getattr(cls, "only_true_extractor", None) != None:
            return cls.only_true_extractor()

        if getattr(cls, "extractor_wheel", None) != None:
            return cls.extractor_wheel(args)

        # dumb way
        for extractor_item in cls.extractors:
            decls = extractor_item.declare_recursive()
            decl = ArgsComparer(decls, args)

            if decl.diff():
                return extractor_item

    async def extract(self, i: dict = {})->dict:
        extract_strategy = self.find_suitable_extractor(i)
        assert extract_strategy != None, "cant find correct extractor"

        extract_strategy_instance = extract_strategy()

        _dict = ArgsComparer(self.declare_recursive(), i, "assert")
        if getattr(self, "before_execute", None) != None:
            self.before_execute(_dict.dict())

        return await extract_strategy_instance.execute(_dict.dict())

    @classmethod
    def describe(cls):
        ps = super().describe()
        ps["variants"] = []
        ps["external_extractors"] = []
        ps["acts"] = []

        for item in cls.receivations:
            ps.get("variants").append(item.describe())

        for item in cls.external_extractors:
            ps.get("external_extractors").append(item.describe())

        for item in cls.acts:
            ps.get("acts").append(item.describe())

        return ps

    @classmethod
    def _build_submodules(cls):
        # assert cls.full_name() != "templates.representations", "submodule of abstract class is used"

        class AbstractAct(Act):
            self_name = "Act"
            outer = cls

        class AbstractReceivation(Extractor):
            self_name = "Extractor"
            outer = cls

            def self_insert(self, item):
                item.mark_representation(self)

        class AbstractExternalExtractor(Extractor):
            self_name = "ExternalExtractor"
            outer = cls

            def self_insert(self, item):
                item.mark_representation(self)

        cls.AbstractAct = AbstractAct
        cls.AbstractReceivation = AbstractReceivation
        cls.AbstractExternalExtractor = AbstractExternalExtractor

    #class ContentUnit(ContentUnit):
    #   pass

    class Thumbnail(ThumbnailMethod):
        pass
