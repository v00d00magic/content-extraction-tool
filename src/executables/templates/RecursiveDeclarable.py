from declarable.ExecutableConfig import ExecutableConfig
from utils.ClassProperty import classproperty

class RecursiveDeclarable:
    executable_cfg =  {}
    consts = {}

    @classproperty
    def executable_configuration(cls):
        if type(cls.executable_cfg) == dict:
            return ExecutableConfig(cls.executable_cfg)

        return cls.executable_cfg

    @classmethod
    def define(cls):
        '''
        Define consts, temp variables etc
        '''

        return {}

    @classmethod
    def declare(cls) -> dict:
        '''
        Method that defines dictionary of current executable args
        '''
        params = {}

        return params

    @classmethod
    def declare_recursive(cls):
        '''
        Brings all params from parent classes to one dict
        '''
        ignore_list = cls.executable_configuration.ignores() # params that will be ignored from current level
        output_params = {}

        for __sub_class in cls.__mro__:
            if hasattr(__sub_class, "define") == True:
                _def = __sub_class.define()

                if _def != None:
                    cls.consts.update(_def)

            # does not have declare function
            if hasattr(__sub_class, "declare") == False:
                continue

            intermediate_dict = {}
            current_level_declaration = __sub_class.declare()
            
            if current_level_declaration == None:
                continue

            for i, name in enumerate(current_level_declaration):
                if name in ignore_list:
                    continue

                intermediate_dict[name] = current_level_declaration.get(name)

            output_params.update(intermediate_dict)

        return output_params
