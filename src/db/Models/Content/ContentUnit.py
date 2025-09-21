from db.Models.Content.ContentModel import ContentModel
from db.Models.Content.StorageUnit import StorageUnit
from peewee import TextField, BooleanField, FloatField, CharField
from utils.Data.Date import Date
from utils.JSONContentContainer import JSONContentContainer
from app.App import logger

class ContentUnit(ContentModel):
    # Display
    display_name = TextField(default='N/A')
    description = TextField(index=True, null=True)

    # Data
    content = TextField(null=True,default=None)
    source = TextField(null=True)
    outer = TextField(null=True,default=None)
    saved = TextField(null=True,default=None)

    # Dates
    declared_created_at = FloatField()
    created_at = FloatField()
    edited_at = FloatField(default=None,null=True)

    # Booleans
    is_collection = BooleanField(index=True,default=0)
    is_unlisted = BooleanField(index=True,default=0)
    # is_deleted = BooleanField(index=True,default=0)

    # Links
    common_link_id = CharField(null=True,max_length=100)

    table_name = 'content_units'
    self_name = 'ContentUnit'
    short_name = 'cu'

    def __init__(self, **kwargs):
        from db.LinkManager import LinkManager

        super().__init__(**kwargs)

        class JSONContentUnitContainer(JSONContentContainer):
            @classmethod
            def get_description(cls):
                return f"{cls.__name__} uuid: {self.uuid}"

        class JSONContent(JSONContentUnitContainer):
            @classmethod
            def get_attr(cls):
                return self.content

            @classmethod
            def set_attr(cls, new_data):
                self.content = cls.attr_json(new_data)

            @classmethod
            def getDataRecursively(cls, recursive = False, recurse_level = 0):
                loaded_content = cls.getData()
                if recursive == True and recurse_level < 3:
                    link_manager = LinkManager(self)
                    loaded_content = link_manager.injectLinksToJsonFromInstance(recurse_level)

                return loaded_content

        class Source(JSONContentUnitContainer):
            @classmethod
            def get_attr(cls):
                return self.source
            
            @classmethod
            def set_attr(cls, new_data):
                self.source = cls.attr_json(new_data)

        class Outer(JSONContentUnitContainer):
            @classmethod
            def get_attr(cls):
                return self.outer

            @classmethod
            def set_attr(cls, new_data):
                self.outer = cls.attr_json(new_data)

        class SavedVia(JSONContentUnitContainer):
            @classmethod
            def get_attr(cls):
                return self.saved

            @classmethod
            def set_attr(cls, new_data):
                self.saved = cls.attr_json(new_data)

            @classmethod
            def sign(cls, method):
                self.via_method = method
                self.SavedVia.update({
                    "method": method.getName(),
                    "representation": method.outer.getName()
                })

        class Links():
            @classmethod
            def checkManager(cls):
                if self.link_manager == None:
                    self.link_manager = LinkManager(self)

            @classmethod
            def getCommon(cls):
                cls.checkManager()
                for item in cls.getLinkedList():
                    if item.uuid == self.common_link_id and item.self_name == "StorageUnit":
                        return item

            @classmethod
            def getLinkedList(cls):
                cls.checkManager()
                logger.log(f"Getting linked from {self.uuid}",section=["Saveable"])

                return self.link_manager.getItems()

            @classmethod
            def markCommon(cls, common_link: StorageUnit):
                cls.checkManager()
                self.common_link_id = common_link.uuid

            @classmethod
            def link(cls, item: ContentModel, is_common: bool = False):
                cls.checkManager()
                self.link_manager.link(item)

                if is_common == True:
                    cls.markCommon(item)

        self.JSONContent = JSONContent
        self.Source = Source
        self.Outer = Outer
        self.SavedVia = SavedVia
        self.Links = Links

        self.link_manager = None
        self.via_method = None

        if self.isSaved() == False:
            _now = Date(Date().now()).timestamp_or_float()

            self.created_at = float(_now)
            self.declared_created_at = float(_now)

    async def beforeSave(self):
        if self.via_method:
            for outer in self.via_method.outer.outerList():
                _outer = outer(self.via_method.outer)

                logger.log(f"Beforesave: run {_outer.getName()}",section="Saveable")

                await _outer.implementation({
                    "item": self
                })

    def getStructure(self, return_content = True, return_linked = True):
        payload = {}
        payload['id'] = str(self.uuid) # Converting to str cuz JSON.parse cannot convert it
        payload['class_name'] = self.self_name
        payload['db'] = self.getDbName()
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
            "created": Date(self.created_at).timestamp_or_float(),
            "edited": Date(self.edited_at).timestamp_or_float(),
            "declared_created": Date(self.declared_created_at).timestamp_or_float()
        }

        if return_linked == True:
            payload["linked"] = []
            for linked_item in self.Links.getLinkedList():
                payload.get("linked").append(linked_item.getStructure())

        return payload
