from .Executable import Executable
from ..ExecutableCall import ExecutableCall

class RepresentationMeta(type):
    def __init__(cls, name, bases, attrs):
        if not name.startswith('_') and bases != (object,):
            cls._build_submodules()
        super().__init__(name, bases, attrs)

class Representation(Executable):
    __metaclass__ = RepresentationMeta
    self_name: str = "Representation"

    @classmethod
    def doDefaultAppending(cls):
        return False

    @classmethod
    def outerList(cls):
        return []

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
        if getattr(cls, "singleExtractor", None) != None:
            return cls.singleExtractor()

        if getattr(cls, "extractorWheel", None) != None:
            return cls.extractorWheel(args)

        if len(cls.receivations) == 1:
            return cls.receivations[0]

        # dumb way
        # Checking all the recieve classes: if it has similar arguments, returning it
        for item in cls.receivations:
            decl = item.comparerShortcut(None, args)

            if decl.diff():
                return item

    async def getOptimalStrategy(self, i: dict = {}):
        strategy = self.findSuitableExtractor(i)

        assert strategy != None, "cant find correct extractor"

        strategy_class = ExecutableCall(None, strategy)
        strategy_class.executable.setOuter(self.__class__)

        return strategy_class

    def variable(self, name):
        return self.strategy.executable.variable(name).get()

    def getResult(self):
        return self.variable("items")

    async def execute(self, i: dict = {}):
        if hasattr(self, "beforeExecute") == True:
            self.beforeExecute(i)

        if getattr(self, "implementation", None) != None:
            return await self.implementation(i)

        self.strategy = await self.getOptimalStrategy(i)
        compares = self.strategy.executable.comparerShortcut(None, i)

        if getattr(self.strategy, "beforeExecute", None) != None:
            self.strategy.beforeExecute(compares.dict())

        response = await self.strategy.executable.execute(compares.dict())
        result = self.getResult()

        return ItemsResponse(result)

    class Source():
        source = {
            "type": "none",
            "content": "str"
        }

    class Content():
        content = {}
