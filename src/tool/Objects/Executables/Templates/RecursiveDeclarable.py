from Objects.classproperty import classproperty
from Plugins.App.Logger.LogParts.LogSection import LogSection
from App import app

class RecursiveDeclarable:
    section_name = "Executables"
    section_name_declarable = ["Executables", "Declaration"]
    section_name_mro = ["Executables", "Declaration", "MRO"]
    consts = {}

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
