from app.Logger.LogSection import LogSection
from app.Logger.LogKind import LogKind
from utils.Data.JSON import JSON

from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Content.StorageUnit import StorageUnit
from db.Links.ContentUnitRelation import RelationEnum

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
        res = self.relations.create(child, relation_type)

        logger.log(message=f"Linked {self.parent.name_db_id}<->{child.name_db_id}, order {res.order}, db: {res.getDbName()}", section = self.section_name, kind = LogKind.KIND_SUCCESS)

        return res

    def linkAsCommon(self, child):
        return self.link(child, RelationEnum.RELATION_MAIN)

    def unlink(self, child, relation_type: int = None) -> bool:
        res = self.relations.remove(child, relation_type)

        logger.log(message=f"Unlinked {self.parent.name_db_id}<->{child.name_db_id}, db: {res.getDbName()}", section = self.section_name, kind = LogKind.KIND_SUCCESS)

        return res != None

    def ids(self, class_name = None, relation_type: int = None):
        items = self.getRelations(class_name, relation_type)
        ids = []

        for item in items:
            ids.append((item.child_type, item.child, item.relation_type))

        return ids

    def getRelations(self, class_name = None, relation_type: int = None):
        return self.relations.getByParent(class_name, relation_type)

    def getModels(self, class_name = None, relation_type: int = None):
        rels = self.getRelations(class_name, relation_type)

        logger.log(message=f"Getting linked from {self.parent.name_db_id}, db {self.parent.getDbName()}", section = self.section_name, kind = LogKind.KIND_SUCCESS)

        return self.relations.relationsToModels(rels)

    def getCommon(self):
        return self.getModels("StorageUnit", RelationEnum.RELATION_MAIN)

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
                            return linked.JSONContent.getDataRecursively(recursive=True,recurse_level=recurse_level+1)

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
        return self.injectLinksToJson(self.parent.JSONContent.getData(), self.getModels(), recurse_level)
