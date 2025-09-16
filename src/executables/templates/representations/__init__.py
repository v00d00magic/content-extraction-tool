from resources.Exceptions import AbstractClassException, SuitableExtractMethodNotFound
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

    @classmethod
    def doDefaultAppending(cls):
        return False

    @classmethod
    def outerList(cls):
        return []

    @classmethod
    def declare(cls):
        params = {}
        params["do_collections"] = BooleanArgument({
            "default": False
        })

        return params

    @classmethod
    def declareRecursive(cls):
        _extractors_args = cls.sumArguments(cls.receivations)

        _fnl = _extractors_args
        _fnl.update(super().declareRecursive())

        return _fnl

    @classmethod
    def sumArguments(cls, extractors):
        _sum = {}
        for extractor_item in extractors:
            rec = extractor_item.declareRecursive()
            for name, item in rec.items():
                _sum[name] = item

        return _sum

    @classmethod
    def divideArguments(cls, extractors):
        _sum = {}
        for extractor_item in extractors:
            _sum[extractor_item.getName()] = extractor_item.declareRecursive()

        return _sum

    @classmethod
    def findSuitableExtractor(cls, args):
        if getattr(cls, "onlyTrueExtractor", None) != None:
            return cls.only_true_extractor()

        if getattr(cls, "extractorWheel", None) != None:
            return cls.extractor_wheel(args)

        if len(cls.receivations) == 1:
            return cls.receivations[0]

        # dumb way
        for item in cls.receivations:
            decl = item.comparerShortcut(None, args)

            if decl.diff():
                return item

    async def optimalStrategy(self, i: dict = {}):
        strategy = self.findSuitableExtractor(i)

        assert strategy != None, "cant find correct extractor"

        strategy_class = strategy()
        compares = strategy_class.comparerShortcut(None, i)

        if getattr(self, "beforeExecute", None) != None:
            self.beforeExecute(compares.dict())

        return await strategy_class.execute(compares.dict())

    async def implementation(self, i: dict = {}):
        return ItemsResponse(await self.optimalStrategy(i))
