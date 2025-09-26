from db.Links.ContentUnitRelation import ContentUnitRelation, RelationEnum
from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Content.StorageUnit import StorageUnit

class Relations:
    def __init__(self, parent = None):
        self.parent = parent

    @property
    def db_reference(self):
        return self.parent._meta.database

    def create(self, child, relation_type: int = RelationEnum.RELATION_NONE):
        assert self.parent != None and child != None, 'Not found item to link'

        parent_id = self.parent.uuid
        child_id = child.uuid

        assert parent_id != None and child_id != None, "Can't link: Ids not assigned"
        assert parent_id != child_id, "Can't link to themselves"

        relation = ContentUnitRelation()
        if self.db_reference != None:
            relation.setDb(self.db_reference)

        relation.parent = parent_id
        relation.child_type = child.__class__.__name__
        relation.child = child_id
        relation.relation_type = relation_type

        relation.save()

        return relation

    def remove(self, child, relation_type: int = RelationEnum.RELATION_NONE) -> bool:
        assert self.parent != None and child != None, 'Not found item to unlink'

        relation_select = ContentUnitRelation()
        if self.db_reference != None:
            relation_select.setDb(self.db_reference)

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
        if self.db_reference != None:
            relation_select.setDb(self.db_reference)

        relation_select = relation_select.select()
        relation_select = relation_select.where(ContentUnitRelation.parent == self.parent.uuid)

        if class_name != None:
            relation_select = relation_select.where(ContentUnitRelation.child_type == class_name)
        if relation_type != None:
            relation_select = relation_select.where(ContentUnitRelation.relation_type == relation_type)

        return relation_select.execute()

    # FIXME refactor
    def relationsToModels(self, items: list, as_dict = False):
        content_units = []
        storage_units = []
        response = []

        for relation in items:
            if relation.child_type == "ContentUnit":
                content_units.append(relation.child)
            else:
                storage_units.append(relation.child)

        if as_dict == True:
            response = {}

            for unit in ContentUnit.select().where(ContentUnit.uuid << content_units):
                response[str(unit.uuid)] = unit
            for unit in StorageUnit.select().where(StorageUnit.uuid << storage_units):
                response[str(unit.uuid)] = unit
        else:
            for unit in ContentUnit.select().where(ContentUnit.uuid << content_units):
                response.append(unit)
            for unit in StorageUnit.select().where(StorageUnit.uuid << storage_units):
                response.append(unit)

        return response
