import asyncio

def category_check(func):
    def wrapper(self, *args, **kwargs):
        category = args[0]
        if self._hooks.get(category) == None:
            self._hooks[category] = []

        return func(self, *args, **kwargs)
    return wrapper

class Hookable:
    categories: list = []
    hooks: dict = {}

    @property
    def events() -> list:
        return []

    def getHooks(self, category) -> list:
        return self._hooks.get(category)

    def runHook(self, hook_func, *args, **kwargs):
        try:
            if asyncio.iscoroutinefunction(hook_func):
                loop = asyncio.get_running_loop()
                loop.create_task(hook_func(*args, **kwargs))
            else:
                hook_func(*args, **kwargs)
        except Exception as e:
            print(e)
            raise e

    @category_check
    def addHook(self, category, hook):
        self.hooks.get(category).append(hook)

    @category_check
    def removeHook(self, category, hook):
        try:
            self.hooks.get(category).remove(hook)
        except Exception:
            pass

    @category_check
    def trigger(self, category, *args, **kwargs):
        for hook in self.hooks.get(category):
            self.runHook(hook, *args, **kwargs)
