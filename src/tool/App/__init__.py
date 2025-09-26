class AppWrapper:
    def __init__(self):
        self._app = None

    def setApp(self, app):
        self._app = app

    def __getattr__(self, name):
        return getattr(self._app, name, None)

app = AppWrapper()
