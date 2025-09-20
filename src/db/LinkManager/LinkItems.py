from db.Models.Relations.ContentUnitRelation import ContentUnitRelation
from db.Models.Content.ContentUnit import ContentUnit
from db.Models.Content.StorageUnit import StorageUnit

class LinkItems:
    def __init__(self, find_where):
        self.find_where = find_where

    def getList(self, class_name = None, relation_type: int = None):
        relations = ContentUnitRelation().select().where(ContentUnitRelation.parent == self.find_where.uuid)
        if class_name != None:
            relations = relations.where(ContentUnitRelation.child_type == class_name)
        if relation_type != None:
            relations = relations.where(ContentUnitRelation.relation_type == relation_type)

        items = []
        for relation in relations:
            items.append(relation)

        return items

    @classmethod
    def idsFromList(cls, items: list, class_name = None, relation_type: int = None):
        ids = []
        for unit in items:
            if class_name != None:
                if unit.child_type == class_name:
                    continue

            if relation_type != None:
                if unit.relation_type == relation_type:
                    continue

            ids.append(unit.child)

        return ids

    @classmethod
    def unitsFromList(cls, items: list, class_name = None, relation_type: int = None):
        content_units = []
        storage_units = []

        for sel in items:
            if sel.child_type == 'ContentUnit':
                content_units.append(sel.child)
            else:
                storage_units.append(sel.child)

        response = []
        for unit in ContentUnit.select().where(ContentUnit.uuid << content_units):
            response.append(unit)
        for unit in StorageUnit.select().where(StorageUnit.uuid << storage_units):
            response.append(unit)

        return response
