from .Template import Template

class Arguments(Template):
    def getList(self):
        return self.outer.model_fields.items()
