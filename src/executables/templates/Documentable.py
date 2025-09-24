from declarable.Documentation import Documentation

class Documentable:
    '''
    Class with description methods
    '''

    def __init_subclass__(cls, **kwargs):
        cls.documentation = Documentation()

        return super().__init_subclass__(**kwargs)

    @classmethod
    def defineMeta(cls):
        return {
            "definition": {
                "en_US": "No description"
            },
        }

    @classmethod
    def key(cls, key_name):
        return cls.documentation.get(key_name)

    @classmethod
    def loadKeys(cls, keys):
        cls.documentation.loadKeys(keys)

    @classmethod
    def getStructure(cls):
        module_name = cls.__module__.split('.')[2:]
        payload = {
            'class': {
                'type': cls.self_name,
                'name': cls.getName(),
                'short': module_name[-1],
                'category': module_name[0]
            },
            'docs': cls.docs,
            'submodules': [],
            'args': [],
        }

        for name, item in cls.declareRecursive().items():
            _arg = item.getStructure()
            _arg["name"] = name

            payload.get("args").append(_arg)

        for item in cls.getSubmodulesByType(None):
            payload.get("submodules").append(item.getStructure())

        return payload
