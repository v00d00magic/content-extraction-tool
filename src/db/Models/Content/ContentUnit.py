from db.Models.Content.Mixin.ThumbnailState import ThumbnailState
from db.Models.Content.Mixin.ThumbnailMixin import ThumbnailMixin
from peewee import TextField, CharField, BooleanField, FloatField
from db.Models.Content.ContentModel import BaseModel
from db.Models.Content.StorageUnit import StorageUnit
from utils.MainUtils import timestamp_or_float, now_timestamp, parse_json, dump_json
from functools import cached_property

class ContentUnit(BaseModel, ThumbnailMixin):
    # Display
    display_name = TextField(default='N/A')
    description = TextField(index=True, null=True)

    # Data
    content = TextField(null=True,default=None)
    source = TextField(null=True)
    outer = TextField(null=True,default=None)
    saved = TextField(null=True,default=None)

    # Links
    storage_unit = CharField(null=True,max_length=100)

    # Dates
    declared_created_at = FloatField()
    created_at = FloatField()
    edited_at = FloatField(default=None,null=True)

    # Booleans
    is_collection = BooleanField(index=True,default=0)
    is_unlisted = BooleanField(index=True,default=0)
    # is_deleted = BooleanField(index=True,default=0)

    table_name = 'content_units'
    self_name = 'ContentUnit'
    short_name = 'cu'

    def __init__(self):
        class ContentContainer():
            _cached = None

            @classmethod
            def get_attr(cls):
                pass

            @classmethod
            def set_attr(cls, new_data):
                pass

            @classmethod
            def get_cached(cls):
                return cls._cached

            @classmethod
            def getData(cls):
                if cls.get_cached() != None:
                    return cls.get_cached()

                if cls.get_attr() == None:
                    return {}

                cls._cached = parse_json(cls.get_attr())
                return cls._cached

            @classmethod
            def update(cls, new_data):
                _data = cls.getData()
                _data.update(new_data)

                cls.set_attr(_data)

            @classmethod
            def get(cls, key, default = None):
                return cls.getData().get(key, default)

        class JSONContent(ContentContainer):
            @classmethod
            def get_attr(cls):
                return self.content

            @classmethod
            def set_attr(cls, new_data):
                self.content = new_data

            @classmethod
            def getDataRecursively(cls, recursive = False, recurse_level = 0):
                from db.LinkManager import LinkManager

                loaded_content = cls.getData()
                if recursive == True and recurse_level < 3:
                    link_manager = LinkManager(self)
                    loaded_content = link_manager.injectLinksToJsonFromInstance(recurse_level)

                return loaded_content

        class Source(ContentContainer):
            @classmethod
            def get_attr(cls):
                return self.source
            
            @classmethod
            def set_attr(cls, new_data):
                self.source = new_data

        class Outer(ContentContainer):
            @classmethod
            def get_attr(cls):
                return self.outer

            @classmethod
            def set_attr(cls, new_data):
                self.outer = new_data

        class SavedVia(ContentContainer):
            @classmethod
            def get_attr(cls):
                return self.saved

            @classmethod
            def set_attr(cls, new_data):
                self.saved = new_data

        self.JSONContent = JSONContent
        self.Source = Source
        self.Outer = Outer
        self.SavedVia = SavedVia

        self.link_queue = []
        self.via_method = None

        return super().__init__()

    @cached_property
    def thumbnail_list(self):
        _thumb = self.outer.get("thumbnail")
        if _thumb == None:
            return []

        _list = []

        for thmb in _thumb:
            _list.append(ThumbnailState(thmb))

        return _list

    @cached_property
    def common_link(self):
        if self.storage_unit != None:
            su = StorageUnit.ids(self.storage_unit)

            return su

        return None

    @cached_property
    def linked_list(self):
        from db.LinkManager import LinkManager

        link_manager = LinkManager(self)
        list = link_manager.linksList(self)

        return list

    def getStructure(self, return_content = True):
        payload = {}
        payload['id'] = str(self.uuid) # Converting to str cuz JSON.parse cannot convert it
        payload['class_name'] = self.self_name
        payload['meta'] = {
            "display_name": self.display_name,
            "description": self.description
        }
        payload['source'] = self.Source.getData()
        payload['saved'] = self.SavedVia.getData()
        payload['outer'] = self.Outer.getData()
        if return_content == True:
            payload['content'] = self.JSONContent.getDataRecursively(recursive=True)

        payload["dates"] = {
            "created": timestamp_or_float(self.created_at),
            "edited": timestamp_or_float(self.edited_at),
            "declared_created": timestamp_or_float(self.declared_created_at)
        }

        return payload

    # it will be saved later
    def link(self, item, is_common: bool = False):
        if self.link_queue is None:
            self.link_queue = []
        if is_common == True:
            self.storage_unit = item.uuid

        self.link_queue.append(item)

    def writeLinkQueue(self):
        from db.LinkManager import LinkManager

        link_manager = LinkManager(self)
        link_manager.writeQueue(self.link_queue)

        self.link_queue = None

    def markSavedJson(self, method):
        self.via_method = method
        self.SavedVia.update({
            "method": method.full_name(),
            "representation": method.outer.full_name()
        })

    def save(self, **kwargs):
        kwargs["force_insert"] = True
        make_thumbnail = True

        self.created_at = float(now_timestamp())

        if getattr(self, "content", None) != None and type(self.content) != str:
            self.JSONContent.update(self.content)

        if getattr(self, "source", None) != None and type(self.source) != str:
            self.Source.update(self.source)

        if self.via_method != None and make_thumbnail == True:
            self.setThumbnail(self.saveThumbnail(self.via_method))

        if getattr(self, "declared_created_at", None) == None:
            self.declared_created_at = float(now_timestamp())

        super().save(**kwargs)

        if self.link_queue != None:
            self.writeLinkQueue()
