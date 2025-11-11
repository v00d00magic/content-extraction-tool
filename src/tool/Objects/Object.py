from pydantic import BaseModel, computed_field
from .Model import Model
from .Hookable import Hookable
from .Section import Section
from .Configurable import Configurable

class Object(Model, Hookable, Section, Configurable):
    pass
