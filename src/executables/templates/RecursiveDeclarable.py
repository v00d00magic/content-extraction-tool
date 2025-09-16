from declarable.ExecutableConfig import ExecutableConfig
from declarable.ArgsComparer import ArgsComparer
from utils.ClassProperty import classproperty

class RecursiveDeclarable:
    consts = {}

    @classmethod
    def executable_cfg(cls):
        pass

    @classproperty
    def executable_configuration(cls):
        _res = cls.executable_cfg()
        if isinstance(_res, ExecutableConfig) == False:
            return ExecutableConfig(_res)

        return _res

    @classmethod
    def define(cls):
        '''
        Define consts, temp variables etc
        '''

        return {}

    @classmethod
    def declare(cls) -> dict:
        '''
        Implementation that defines dictionary of current executable args
        '''
        params = {}

        return params

    def comparerShortcut(self, declare_with, args):
        if declare_with == None:
            declare_with = self.__class__.declareRecursive()

        self.executable_configuration.check()

        return ArgsComparer(compare=declare_with, 
                            args=args,
                            exc='assert', 
                            missing_args_inclusion=self.executable_configuration.is_free_args(), 
                            default_sub=self.doDefaultAppending())

    @classmethod
    def declareRecursive(cls):
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
