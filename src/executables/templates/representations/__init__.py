from resources.Exceptions import AbstractClassException, SuitableExtractMethodNotFound
from thumbnails import ThumbnailMethod
from declarable.ArgsComparer import ArgsComparer
from declarable.Arguments import BooleanArgument
from executables.templates.Executable import Executable
from executables.responses.ItemsResponse import ItemsResponse

class RepresentationMeta(type):
    def __init__(cls, name, bases, attrs):
        if not name.startswith('_') and bases != (object,):
            cls._build_submodules()
        super().__init__(name, bases, attrs)

class Representation(Executable, metaclass=RepresentationMeta):
    self_name = "Representation"
    _default_sub = False

    @classmethod
    def declare(cls):
        params = {}
        params["do_collections"] = BooleanArgument({
            "default": False
        })

        return params

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

        if len(cls.receivations) == 1:
            return cls.receivations[0]

        # dumb way
        for extractor_item in cls.receivations:
            decls = extractor_item.declare_recursive()
            decl = ArgsComparer(decls, args)

            if decl.diff():
                return extractor_item

    async def extract(self, i: dict = {}):
        extract_strategy = self.find_suitable_extractor(i)
        assert extract_strategy != None, "cant find correct extractor"

        extract_strategy_instance = extract_strategy()

        _dict = ArgsComparer(self.declare_recursive(), i, "assert")
        if getattr(self, "beforeExecute", None) != None:
            self.beforeExecute(_dict.dict())

        return await extract_strategy_instance.execute(_dict.dict())

    async def implementation(self, i: dict = {}):
        return ItemsResponse(await self.extract(i))

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

    #class ContentUnit(ContentUnit):
    #   pass

    class Thumbnail(ThumbnailMethod):
        pass
