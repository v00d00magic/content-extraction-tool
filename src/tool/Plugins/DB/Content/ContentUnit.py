from ..Model import Model
from datetime import datetime
from Objects.Object import Object
from pydantic import Field, ConfigDict, field_serializer
from DB.Models.ContentUnit import ContentUnit as _cu
from typing import ClassVar

# you need to extend this in representations
class ContentUnit(Model):
    orm: ClassVar = _cu

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

    content: ContentData # if you extend ContentData you should duplicate annotation too
    source: Source
    outer: Outer = Field(default = Outer())
    saved: Saved

    created_at: datetime = Field(default_factory=lambda: datetime.now())
    declared_created_at: datetime = Field(default_factory=lambda: datetime.now())
    edited_at: datetime = Field(default=None)

    is_collection: bool = Field(default=False)
    is_unlisted: bool = Field(default=False)

    links: Links = Field(default=None)

    @field_serializer('created_at', 'declared_created_at', 'edited_at')
    def serialize_date(self, dt: datetime) -> float:
        if dt == None:
            return None

        return float(dt.timestamp())
