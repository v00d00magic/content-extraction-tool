from ..Model import Model
from .Items.Outer import Outer
from .Items.Saved import Saved
from .Items.Source import Source
from .Items.Links import Links
from datetime import datetime
from pydantic import Field
from typing import List

class ContentUnit(Model):
    display_name: str = Field()
    display_description: str = Field()
    original_name: str = Field()
    original_description: str = Field()
    index_description: str = Field()

    content: dict = Field()
    source: Source = Field(default=None)
    outer: Outer = Field(default=None)
    saved: Saved = Field(default=None)

    created_at: datetime = Field(default_factory=lambda: datetime.now())
    declared_created_at: datetime = Field(default_factory=lambda: datetime.now())
    edited_at: datetime = Field(default=None)

    is_collection: bool = Field(default=False)
    is_unlisted: bool = Field(default=False)

    links: Links = Field(default=None)
