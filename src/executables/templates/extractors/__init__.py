from executables.templates.Executable import Executable

class Extractor(Executable):
    self_name = "Extractor"
    link_after = []
    linked_dict = None
    base_categories = ["template", "base", "extractors"]

    def subscribe(self, linked_dict: dict):
        self.linked_dict = linked_dict

    def link_after_add(self, item):
        self.link_after.append(item)
