from Declarable.Arguments.Argument import Argument

class ContentUnitArgument(Argument):
    def implementation(self):
        from DB.Models.Content.ContentUnit import ContentUnit

        if self.passed_value != None:
            item = ContentUnit.ids(self.passed_value)

            return item
