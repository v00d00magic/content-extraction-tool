from .Response import Response
from pydantic import Field
from typing import List

class ModelsResponse(Response):
    data: List = Field(default = [])
