class LogLimiter():
    def __init__(self, skip_categories):
        self.skip_categories = skip_categories

    def shouldBeDisplayed(self, msg, where):
        for _section in self.skip_categories:
            if _section.isIt(msg.section, msg.kind) == True:
                return _section.where != where

        return True
