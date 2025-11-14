from ..Model import Model
from datetime import datetime
from Objects.Object import Object
from pydantic import Field, ConfigDict, field_serializer
from DB.Models.ContentUnit import ContentUnit as _cu
from typing import ClassVar

# you may to extend this in your classes
class ContentUnit(Model):
    orm_model: ClassVar = _cu

    class Data(Object):
        '''
        Data that will be flushed into 'Content' column as JSON
        You need to provide pydantic annotations for your keys
        Also after extending the class the annotations will be old, so you must add:

        content: Data

        to your extended class to apply the new fields. This is also necessary to, idk how to name it, containers,
        Source, Saved, Outer.

        I've been deleting duplicated logics last days and this is maybe the last part with duplicated logics.
        So todo, save every class's field? I think its better to leave as is

        TODO add ContentUnit.Data.Extension for more harder structures
        '''
        model_config = ConfigDict(extra='allow')

    class Source(Object):
        types: str = Field(default = None)
        content: str = Field(default = None)

    class Saved(Object):
        name: str = Field(default = None)
        method: str = Field(default = None)
        call: int = Field(default = None)

    class Outer(Object):
        thumbnail: dict = Field(default = None)
        time: dict = Field() # duration

    class Links(Object):
        items: list = Field()

    display_name: str = Field(default=None)
    display_description: str = Field(default=None)
    original_name: str = Field(default=None)
    original_description: str = Field(default=None)
    index_description: str = Field(default=None)

    content: Data # if you extend Data you should duplicate annotation too
    source: Source = Field(default = None)
    outer: Outer = Field(default = None)
    saved: Saved = Field(default = None)

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
