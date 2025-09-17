from db.Models.Content.ContentModel import ContentModel
from db.Models.Content.StorageUnit import StorageUnit
from peewee import TextField, BooleanField, FloatField, CharField
from utils.MainUtils import timestamp_or_float, now_timestamp, parse_json
from app.App import logger, db_connection

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

    def __init__(self):
        super().__init__()

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
                logger.log(f"getting {cls.__name__} property",section=["Saveable", "Container"])

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

                logger.log(f"Updated container {cls.__name__}",section=["Saveable", "Container"])

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
        self.common_link = None

        if self.isSaved() == False:
            _now = now_timestamp()
            if self.common_link_id != None:
                self.common_link = StorageUnit.ids(int(self.common_link_id))

            self.created_at = float(_now)
            self.declared_created_at = float(_now)

    def getLinkedList(self):
        from db.LinkManager import LinkManager

        logger.log(f"Getting linked from {self.uuid}",section=["Saveable"])

        link_manager = LinkManager(self)

        return link_manager.linksList()

    def getStructure(self, return_content = True, return_linked = True):
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

        if return_linked == True:
            payload["linked"] = []
            for linked_item in self.getLinkedList():
                payload.get("linked").append(linked_item.getStructure())

        return payload

    def markCommon(self, common_link: StorageUnit):
        self.common_link = common_link
        self.common_link_id = common_link.uuid

    def signRepresentation(self, method):
        self.via_method = method
        self.SavedVia.update({
            "method": method.getName(),
            "representation": method.outer.getName()
        })

    # Links

    def link(self, item, is_common: bool = False):
        if is_common == True:
            self.markCommon(item)

        self.link_queue.append(item)

    def writeLinkQueue(self):
        from db.LinkManager import LinkManager

        link_manager = LinkManager(self)
        link_manager.writeQueue(self.link_queue)

        self.link_queue = []

    def isQueued(self):
        return self.isSaved()

    # Hooks

    async def beforeSave(self):
        if self.via_method:
            for outer in self.via_method.outer.outerList():
                _outer = outer(self.via_method.outer)

                logger.log(f"Beforesave: run {_outer.getName()}",section="Saveable")

                await _outer.implementation({
                    "item": self
                })

    def postSave(self):
        logger.log(f"Saved ContentUnit, saved id: {self.uuid} to db temp, trying to link {len(self.link_queue)} items",section="Saveable")

        if len(self.link_queue) > 0:
            self.writeLinkQueue()

    # saving to temporary db
    def save(self, **kwargs):
        kwargs["force_insert"] = True

        to_db = kwargs.get("db")
        if to_db == None:
            to_db = db_connection.temp_db

        self.setDb(to_db)

        super().save(**kwargs)
        self.postSave()

