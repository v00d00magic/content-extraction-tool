from db.Links.ContentUnitRelation import ContentUnitRelation, RelationEnum

class Relations:
    def __init__(self, parent = None):
        self.parent = parent

    @property
    def db_reference(self):
        return self.parent._meta.database

    def create(self, parent, child, relation_type: int = RelationEnum.RELATION_NONE):
        assert parent != None and child != None, 'Not found item to link'

        parent_id = parent.uuid
        child_id = child.uuid

        assert parent_id != None and child_id != None, "Can't link: Ids not assigned"
        assert parent_id != child_id, "Can't link to themselves"

        relation = ContentUnitRelation()
        if self.db_reference != None:
            relation.setDb(self.db_reference)

        relation.parent = parent_id
        relation.child_type = child.__class__.__name__
        relation.child = child_id
        if relation_type != None:
            relation.relation_type = relation_type

        relation.save()

        return relation

    def remove(self, parent, child, relation_type: int = RelationEnum.RELATION_NONE) -> bool:
        assert parent != None and child != None, 'Not found item to unlink'

        relation_select = ContentUnitRelation()
        if self.db_reference != None:
            relation_select.setDb(self.db_reference)

        relation_select = relation_select.select()
        relation_select = relation_select.where(ContentUnitRelation.parent == parent.uuid)
        relation_select = relation_select.where(ContentUnitRelation.child == child.uuid)
        relation_select = relation_select.where(ContentUnitRelation.child_type == child.__class__.__name__)
        if relation_type != None:
            relation_select = relation_select.where(ContentUnitRelation.relation_type == relation_type)

        if relation_select == None:
            return False
        
        relation_select.delete()

        return True

    def getByParent(self, parent, class_name: str = None, relation_type: int = RelationEnum.RELATION_NONE) -> list:
        relation_select = ContentUnitRelation()
        if self.db_reference != None:
            relation_select.setDb(self.db_reference)

        relation_select = relation_select.select()
        relation_select = relation_select.where(ContentUnitRelation.parent == parent.uuid)

        if class_name != None:
            relation_select = relation_select.where(ContentUnitRelation.child_type == class_name)
        if relation_type != None:
            relation_select = relation_select.where(ContentUnitRelation.relation_type == relation_type)

        return relation_select.execute()
