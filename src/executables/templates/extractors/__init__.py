from executables.templates.Executable import Executable
from executables.templates.Documentable import Documentable
from executables.templates.Runnable import Runnable
from executables.templates.Saveable import Saveable
from executables.templates.RecursiveDeclarable import RecursiveDeclarable

class Extractor(Executable):
    self_name = "Extractor"
    link_after = []
    linked_dict = None
    base_categories = ["template", "base", "extractors"]

    def subscribe(self, linked_dict: dict):
        self.linked_dict = linked_dict

    def link_after_add(self, item):
        self.link_after.append(item)

class BaseExtractor(Runnable, Documentable, Saveable, RecursiveDeclarable):
    self_name = "Extractor"
