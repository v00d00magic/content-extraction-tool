from ..Model import Model
from .Items.Outer import Outer
from .Items.Saved import Saved
from .Items.Source import Source
from .Items.Links import Links
from datetime import datetime
from Objects.Object import Object
from pydantic import Field

class ContentUnit(Model):
    display_name: str = Field(default=None)
    display_description: str = Field(default=None)
    original_name: str = Field(default=None)
    original_description: str = Field(default=None)
    index_description: str = Field(default=None)

    content: Object
    source: Source
    outer: Outer
    saved: Saved

    created_at: datetime = Field(default_factory=lambda: datetime.now())
    declared_created_at: datetime = Field(default_factory=lambda: datetime.now())
    edited_at: datetime = Field(default=None)

    is_collection: bool = Field(default=False)
    is_unlisted: bool = Field(default=False)

    links: Links = Field(default=None)
