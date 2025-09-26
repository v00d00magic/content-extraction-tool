from Declarable.ExecutableConfig import ExecutableConfig
from Declarable.Arguments.ArgsComparer import ArgsComparer
from Utils.ClassProperty import classproperty
from App.Logger.LogSection import LogSection
from App import app

class RecursiveDeclarable:
    section_name = "Executables"
    section_name_declarable = ["Executables", "Declaration"]
    section_name_mro = ["Executables", "Declaration", "MRO"]
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

    @classmethod
    def comparerShortcut(cls, declare_with, args):
        app.logger.log(f"Called ArgsComparer to {cls.getName()}", section = cls.section_name)
        if declare_with == None:
            declare_with = cls.declareRecursive()

        cls.executable_configuration.check()

        return ArgsComparer(compare=declare_with, 
                            args=args,
                            exc='assert', 
                            missing_args_inclusion=cls.executable_configuration.is_free_args(), 
                            default_sub=cls.doDefaultAppending())

    @classmethod
    def declareRecursive(cls):
        '''
        Brings all params from parent classes to single dict
        '''
        ignore_list = cls.executable_configuration.ignores() # params that will be ignored from current level
        output_params = {}

        app.logger.log("Called recursive declaration...", section = cls.section_name_declarable)

        for _sub_class in cls.__mro__:
            if hasattr(_sub_class, "define") == True:
                _def = _sub_class.define()

                if _def != None:
                    cls.consts.update(_def)

            # does not have declare function
            if hasattr(_sub_class, "declare") == False:
                continue

            count = 0
            intermediate_dict = {}
            current_level_declaration = _sub_class.declare()
            if current_level_declaration == None:
                continue

            for i, name in enumerate(current_level_declaration):
                if name in ignore_list:
                    continue

                count += 1
                intermediate_dict[name] = current_level_declaration.get(name)

            app.logger.log(f"Class {cls.getName()}: Called declare at {_sub_class.__name__} and got {count} arguments", section = cls.section_name_mro)

            output_params.update(intermediate_dict)

        return output_params
