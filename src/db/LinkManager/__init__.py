from db.Models.Relations.ContentUnitRelation import ContentUnitRelation
from db.LinkManager.LinkItems import LinkItems
from app.Logger.LogSection import LogSection
from app.Logger.LogKind import LogKind
from app.App import logger

class AlreadyLinkedException(Exception):
    pass

class LinkManager:
    def __init__(self, parent):
        self.parent = parent
        self.items = LinkItems(self.parent).getList()

    def __check_if_already_linked_somewhere(self, child):
        for relation in self.items:
            if relation.child_type == child.short_name and relation.child == child.uuid:
                raise AlreadyLinkedException(f"{relation.short_name}_{relation.uuid} already linked somewhere")

    def link(self, child, relation_type: int = None) -> ContentUnitRelation:
        assert self.parent != None and child != None, 'Not found item to link'
        assert self.parent.uuid != None and child.uuid != None, "Can't link: Items probaly not saved"
        assert self.parent.uuid != child.uuid, "Can't link to themselves"

        self.__check_if_already_linked_somewhere(child)

        relation = ContentUnitRelation()
        relation.parent = self.parent.uuid
        relation.child_type = child.__class__.__name__
        relation.child = child.uuid
        if relation_type != None:
            relation.relation_type = relation_type

        relation.save()

        self.items.append(relation)

        logger.log(message=f"Linked {self.parent.short_name}_{self.parent.uuid}<->{child.short_name}_{child.uuid}", section=LogSection.SECTION_LINKAGE, kind = LogKind.KIND_SUCCESS)

        return relation

    def unlink(self, child, relation_type: int = None) -> bool:
        assert self.parent != None and child != None, 'Not found item to unlink'

        relation = ContentUnitRelation().select().where(ContentUnitRelation.parent == self.parent.uuid).where(ContentUnitRelation.child == child.uuid).where(ContentUnitRelation.child_type == child.__class__.__name__)
        if relation_type != None:
            relation = relation.where(ContentUnitRelation.relation_type == relation_type)

        if relation == None:
            return True

        relation.delete()

        # add code for removing from self.items

        logger.log(message=f"Unlinked {self.parent.short_name}_{self.parent.uuid}<->{child.short_name}_{child.uuid}", section=LogSection.SECTION_LINKAGE, kind = LogKind.KIND_SUCCESS)

        return True


    def ids(self, class_name = None, relation_type: int = None):
        return LinkItems.idsFromList(self.items)

    def getItems(self, class_name = None, relation_type: int = None):
        return LinkItems.unitsFromList(self.items)

    def injectLinksToJson(self, to_check, linked_list, recurse_level = 0, recurse_limit = 10):
        if isinstance(to_check, dict):
            return {key: self.injectLinksToJson(value, linked_list) for key, value in to_check.items()}
        elif isinstance(to_check, list):
            return [self.injectLinksToJson(item, linked_list) for item in to_check]
        elif isinstance(to_check, str):
            try:
                if to_check.startswith("__$|cu_"):
                    got_id = to_check.replace("__$|cu_", "")
                    got_id = int(got_id)

                    for linked in linked_list:
                        if linked.uuid == got_id and linked.self_name == "ContentUnit":
                            return linked.data_with_linked_replacements(recursive=True,recurse_level=recurse_level+1)

                    return to_check
                elif to_check.startswith("__$|su_"):
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
        return self.injectLinksToJson(self.parent.JSONContent.getData(), self.items, recurse_level)
