class ViewWrapper:
    '''
    Allows to access current view
    '''

    def __init__(self):
        self._view = None

    def mount(self, name, item):
        # print(f'set global {name}')

        setattr(self._view.app.app, name, item)

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
            return self._view.app.app.settings

        return getattr(self._view.app.app, name, None)

app = ViewWrapper()
