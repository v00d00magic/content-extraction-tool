from ..Model import Model
from datetime import datetime
from Objects.Object import Object
from pydantic import Field, ConfigDict

class ContentUnit(Model):
    class ContentData(Object):
        model_config = ConfigDict(extra='allow')

    class Source(Object):
        types: str = Field(default = None)
        content: str = Field(default = None)

    class Saved(Object):
        representation: str = Field(default = None)
        method: str = Field(default = None)

    class Outer(Object):
        thumbnail: dict = Field(default = None)

    class Links(Object):
        items: list = Field()

    display_name: str = Field(default=None)
    display_description: str = Field(default=None)
    original_name: str = Field(default=None)
    original_description: str = Field(default=None)
    index_description: str = Field(default=None)

    content: ContentData
    source: Source
    outer: Outer = Field(default = Outer())
    saved: Saved

    created_at: datetime = Field(default_factory=lambda: datetime.now())
    declared_created_at: datetime = Field(default_factory=lambda: datetime.now())
    edited_at: datetime = Field(default=None)

    is_collection: bool = Field(default=False)
    is_unlisted: bool = Field(default=False)

    links: Links = Field(default=None)
