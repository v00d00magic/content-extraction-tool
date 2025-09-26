import asyncio

def category_check(func):
    def wrapper(self, *args, **kwargs):
        category = args[0]
        if self._hooks.get(category) == None:
            self._hooks[category] = []

        return func(self, *args, **kwargs)
    return wrapper

class Hookable:
    events = []

    def __init__(self):
        self._hooks = {}

    def hooks(self, category):
        return self._hooks.get(category)

    def run_hook(self, hook_func, *args, **kwargs):
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
    def add_hook(self, category, hook):
        self._hooks.get(category).append(hook)

    @category_check
    def remove_hook(self, category, hook):
        try:
            self._hooks.get(category).remove(hook)
        except Exception:
            pass

    @category_check
    def trigger(self, category, *args, **kwargs):
        for hook in self._hooks.get(category):
            self.run_hook(hook, *args, **kwargs)
