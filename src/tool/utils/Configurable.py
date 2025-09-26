from App.Config.DefaultSettings import DefaultSettings

class Configurable:
    @classmethod
    def updateConfig(cls):
        DefaultSettings.update(cls.declareSettings())

    @classmethod
    def declareSettings(cls):
        pass
