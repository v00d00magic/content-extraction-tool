from declarable.Documentation import Documentation

class Documentable:
    '''
    Class with description methods
    '''

    def __init_subclass__(cls, **kwargs):
        cls.documentation = Documentation()

        return super().__init_subclass__(**kwargs)

    @classmethod
    def define_meta(cls):
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
    def describe(cls):
        module_name = cls.__module__.split('.')[2:]

        ts = {
            'type': cls.self_name,
            'category': module_name[0],
            'class': cls.full_name(),
            'name': module_name[-1],
            'docs': cls.docs,
            'args': [],
        }

        _args = cls.declare_recursive()
        for _name, _item in _args.items():
            _p = _args.get(_name).describe()

            _p['name'] = _name
            ts['args'].append(_p)

        if getattr(cls, "PreExecute", None) != None:
            pre_exec = cls.PreExecute

            ts["confirmation"] = pre_exec.args_list

        return ts
