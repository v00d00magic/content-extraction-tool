from Objects.Outer import Outer
from pydantic import PrivateAttr, Field
from pydantic.dataclasses import dataclass
from typing import ClassVar, Any
import asyncio

class Hookable():
    hooks: ClassVar[Any] = PrivateAttr(default = None)

    def init_subclass(cls):
        cls.hooks = cls.HooksManager()
        for category in cls.hooks.events:
            cls.hooks.items[category] = []

    @dataclass
    class HooksManager:
        items: dict = Field(default = {})
        categories: list = Field(default = [])

        @property
        def events(self) -> list:
            return []

        def register(self):
            pass

        def get(self, category: str) -> list:
            return self.items.get(category)

        def run(self, hook_func, *args, **kwargs) -> None:
            try:
                if asyncio.iscoroutinefunction(hook_func):
                    loop = asyncio.get_running_loop()
                    loop.create_task(hook_func(*args, **kwargs))
                else:
                    hook_func(*args, **kwargs)
            except Exception as e:
                print(e)
                raise e

        def add(self, category: str, hook) -> None:
            if self.items.get(category) == None:
                self.items[category] = []

            self.items.get(category).append(hook)

        def remove(self, category: str, hook) -> None:
            try:
                self.items.get(category).remove(hook)
            except Exception:
                pass

        def trigger(self, category: str, *args, **kwargs) -> None:
            for hook in self.items.get(category):
                self.run(hook, *args, **kwargs)
