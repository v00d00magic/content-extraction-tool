from DB.Links.ContentUnitRelation import ContentUnitRelation, RelationEnum
from DB.Models.Content.ContentUnit import ContentUnit
from DB.Models.Content.StorageUnit import StorageUnit

class Relations:
    def __init__(self, parent = None):
        self.parent = parent
        self.wrapper = None

    def setWrapper(self, wrapper):
        self.wrapper = wrapper

    def create(self, child, relation_type: int = RelationEnum.RELATION_NONE):
        assert self.parent != None and child != None, 'Not found item to link'

        parent_id = self.parent.uuid
        child_id = child.uuid

        assert parent_id != None and child_id != None, "Can't link: Ids not assigned"
        assert parent_id != child_id, "Can't link to themselves"

        relation = ContentUnitRelation()

        if self.wrapper != None:
            relation.setWrapper(self.wrapper)
            relation.bind(self.wrapper.db_ref)

        relation.parent = parent_id
        relation.child_type = child.__class__.__name__
        relation.child = child_id
        relation.relation_type = relation_type

        relation.save()

        return relation

    def remove(self, child, relation_type: int = RelationEnum.RELATION_NONE) -> bool:
        assert self.parent != None and child != None, 'Not found item to unlink'

        relation_select = ContentUnitRelation()
        if self.wrapper != None:
            relation_select.setWrapper(self.wrapper)

        relation_select = relation_select.select()
        relation_select = relation_select.where(ContentUnitRelation.parent == self.parent.uuid)
        relation_select = relation_select.where(ContentUnitRelation.child == child.uuid)
        relation_select = relation_select.where(ContentUnitRelation.child_type == child.__class__.__name__)
        if relation_type != None:
            relation_select = relation_select.where(ContentUnitRelation.relation_type == relation_type)

        if relation_select == None:
            return False

        relation_select.delete()

        return True

    def getByParent(self, class_name: str = None, relation_type: int = RelationEnum.RELATION_NONE) -> list:
        relation_select = ContentUnitRelation()
        if self.wrapper != None:
            relation_select.setWrapper(self.wrapper)

        relation_select = relation_select.select()
        relation_select = relation_select.where(ContentUnitRelation.parent == self.parent.uuid)

        if class_name != None:
            relation_select = relation_select.where(ContentUnitRelation.child_type == class_name)
        if relation_type != None:
            relation_select = relation_select.where(ContentUnitRelation.relation_type == relation_type)

        items = []
        for item in relation_select.execute():
            if self.wrapper != None:
                item.setWrapper(self.wrapper)

            items.append(item)

        return items

    @staticmethod
    def splitItems(items):
        ids = {
            "c": [],
            "s": []
        }

        for relation in items:
            if relation.child_type == "ContentUnit":
                ids.get("c").append(relation.child)
            else:
                ids.get("s").append(relation.child)

        return ids

    def relationsToModels(self, items: list, as_dict = False):
        ids = self.splitItems(items)
        response = {}

        # :(
        # TODO refactor

        _c = ContentUnit()
        _s = StorageUnit()

        if self.wrapper != None:
            _c.setWrapper(self.wrapper)
            _s.setWrapper(self.wrapper)

            with self.wrapper.db_ref.bind_ctx([_c, _s]):
                _c = _c.select().where(ContentUnit.uuid << ids.get("c")).execute()
                _s = _s.select().where(StorageUnit.uuid << ids.get("s")).execute()

        for unit in _c:
            response[str(unit.uuid)] = unit
        for unit in _s:
            response[str(unit.uuid)] = unit

        if as_dict == False:
            return response.values()

        return response
