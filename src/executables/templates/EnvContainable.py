class EnvContainable:
    '''
    Class that contains env variables
    '''
    @classmethod
    def getEnvVars(cls):
        res = {}
        for __sub_class in cls.__mro__:
            if getattr(__sub_class, "declareEnv", None) != None:
                res.update(__sub_class.declareEnv())

        return res

    @classmethod
    def declareEnv(cls):
        return {}

    @classmethod
    def env(cls, name):
        arg = cls.getEnvVars().get(name)
        arg.configuration["name"] = name

        return arg
