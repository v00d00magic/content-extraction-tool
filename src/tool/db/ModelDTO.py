from App import app

class ModelDTO:
    def moveTo(self,
               item, 
               db,
               recursion_value = 0,
               recursion_limit = 10):
        counts = 0
        links = []

        if getattr(item, "LinkManager", None) != None:
            relations = item.LinkManager.getRelations()

            app.logger.log(f"Found {len(relations)} linked at {item.name_db_id}", section=["Saveable"])

            for link_item in relations:
                links.append(link_item.getStructure())

        item.setDb(db)

        app.logger.log(f"Set db of item {item.name_db_id} to {item.getDbName()}", section=["Saveable", "DB"])

        if hasattr(item, "moveSelf") == True:
            item.moveSelf()

        item.save()

        if recursion_value > recursion_limit:
            return

        for link_obj in links:
            link_item = link_obj.get("item")
            link_type = link_obj.get("type")

            movement = ModelDTO()
            movement.moveTo(item = link_item, 
                            db = db, 
                            recursion_value = recursion_value + 1,
                            recursion_limit = recursion_limit)
            item.LinkManager.link(link_item, link_type)

        return counts
