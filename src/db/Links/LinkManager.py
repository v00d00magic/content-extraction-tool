from app.Logger.LogSection import LogSection
from app.Logger.LogKind import LogKind
from utils.Data.JSON import JSON

from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Content.StorageUnit import StorageUnit

from db.Links.Relations import Relations
from app.App import logger

class AlreadyLinkedException(Exception):
    pass

class LinkManager:
    section_name = "LinkManager"

    def __init__(self, parent: ContentUnit):
        self.parent = parent
        self.relations = Relations(self.parent)

    def __check_if_already_linked_somewhere(self, child):
        for relation in self.items:
            if relation.child_type == child.short_name and relation.child == child.uuid:
                raise AlreadyLinkedException(f"{relation.short_name}_{relation.uuid} already linked somewhere")

    def link(self, child, relation_type: int = None):
        res = self.relations.create(self.parent, child, relation_type)

        logger.log(message=f"Linked {self.parent.name_db_id}<->{child.name_db_id}, order {res.order}, db: {res.getDbName()}", section = self.section_name, kind = LogKind.KIND_SUCCESS)

        return res

    def unlink(self, child, relation_type: int = None) -> bool:
        res = self.relations.remove(self.parent, child, relation_type)

        logger.log(message=f"Unlinked {self.parent.name_db_id}<->{child.name_db_id}, db: {res.getDbName()}", section = self.section_name, kind = LogKind.KIND_SUCCESS)

        return res != None

    def ids(self, class_name = None, relation_type: int = None):
        items = self.relations.getByParent(self.parent, class_name, relation_type)
        ids = []

        for item in items:
            ids.append((item.child_type, item.child, item.relation_type))

        return ids

    def getItems(self, class_name = None, relation_type: int = None):
        content_units = []
        storage_units = []
        response = []

        logger.log(message=f"Getting linked from {self.parent.name_db_id}, db {self.parent.getDbName()}", section = self.section_name, kind = LogKind.KIND_SUCCESS)

        for id in self.ids(class_name, relation_type):
            if id[0] == 'ContentUnit':
                content_units.append(id[1])
            else:
                storage_units.append(id[1])

        for unit in ContentUnit.select().where(ContentUnit.uuid << content_units):
            response.append(unit)
        for unit in StorageUnit.select().where(StorageUnit.uuid << storage_units):
            response.append(unit)

        return response

    def injectLinksToJson(self, to_check, linked_list, recurse_level = 0, recurse_limit = 10):
        if isinstance(to_check, dict):
            return {key: self.injectLinksToJson(value, linked_list) for key, value in to_check.items()}
        elif isinstance(to_check, list):
            return [self.injectLinksToJson(item, linked_list) for item in to_check]
        elif isinstance(to_check, str):
            try:
                if to_check.startswith(ContentUnit.link_sign):
                    got_id = to_check.replace("__$|cu_", "")
                    got_id = int(got_id)

                    for linked in linked_list:
                        if linked.uuid == got_id and linked.self_name == "ContentUnit":
                            return linked.data_with_linked_replacements(recursive=True,recurse_level=recurse_level+1)

                    return to_check
                elif to_check.startswith(StorageUnit.link_sign):
                    got_id = to_check.replace("__$|su_", "")
                    got_id = int(got_id)
                    for linked in linked_list:
                        if linked.uuid == got_id and linked.self_name == "StorageUnit":
                            return linked.getStructure()

                    return to_check
                else:
                    return to_check
            except Exception as exception:
                logger.log(exception, section="Linkage")
                return to_check
        else:
            return to_check

    def injectLinksToJsonFromInstance(self, recurse_level = 0):
        return self.injectLinksToJson(self.parent.JSONContent.getData(), self.getItems(), recurse_level)
