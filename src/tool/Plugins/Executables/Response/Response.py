from Objects.Object import Object
from pydantic import Field
from typing import Any

class Response(Object):
    data: Any = Field(default = None)

    def toDict(self) -> Any:
        return self.data
