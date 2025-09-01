from executables.templates.Executable import Executable
from executables.templates.Documentable import Documentable
from executables.templates.Runnable import Runnable
from executables.templates.Saveable import Saveable
from executables.templates.RecursiveDeclarable import RecursiveDeclarable

class Act(Executable):
    self_name = "Act"

class BaseAct(Runnable, Documentable, Saveable, RecursiveDeclarable):
    self_name = "Act"
