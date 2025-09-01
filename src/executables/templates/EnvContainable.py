from utils.ClassProperty import classproperty

class EnvContainable:

    @classproperty
    def env_vars(cls):
        res = {}
        for __sub_class in cls.__mro__:
            if getattr(__sub_class, "declare_env", None) != None:
                res.update(__sub_class.declare_env())

        return res

    @classmethod
    def declare_env(cls):
        return {}

    @classmethod
    def env(cls, name):
        arg = cls.env_vars.get(name)
        arg.configuration["name"] = name

        return arg
