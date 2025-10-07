class ViewWrapper:
    def __init__(self):
        self._view = None

    def setView(self, view):
        self._view = view

    def __getattr__(self, name):
        if name == "settings":
            return self._view.app_wrapper.app.settings

        return getattr(self._view.app_wrapper.app, name, None)

app = ViewWrapper()
