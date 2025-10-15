from Objects.Object import Object
from pydantic import ConfigDict

# you must define this at representation

class Content(Object):
    model_config = ConfigDict(extra='allow')
