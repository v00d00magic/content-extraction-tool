from .Response import Response
from pydantic import Field
from typing import List

class ModelsResponse(Response):
    data: List = Field(default = [])

    def toDict(self) -> list:
        out = []

        for item in self.data:
            print(item)
            out.append(item.toJson())

        return out
