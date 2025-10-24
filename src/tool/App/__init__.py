class ViewWrapper:
    '''
    Allows to access current view
    '''

    def __init__(self):
        self._view = None

    def setView(self, view):
        '''
        Sets the global view and app that can be accessed via

        from App import app
        '''

        self._view = view

    def __getattr__(self, name):
        '''
        Allows to use classes like Logger, Storage ... :

        app.Logger.log(...)
        '''

        if name == "settings":
            return self._view.app_wrapper.app.settings

        return getattr(self._view.app_wrapper.app, name, None)

app = ViewWrapper()
