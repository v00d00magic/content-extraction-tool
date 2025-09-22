from app.App import logger

class ModelDTO:
    def moveTo(self, 
               item, 
               db,
               recursion_value = 0,
               recursion_limit = 10):
        counts = 0
        links = []

        if getattr(item, "LinkManager", None) != None:
            linked_items = item.LinkManager.getItems()

            logger.log(f"Found {len(linked_items)} linked at {item.getDbName()}:{item.uuid}", section=["Saveable"])

            for link_item in linked_items:
                links.append(link_item)

        item.setDb(db)
        if hasattr(item, "moveSelf") == True:
            item.moveSelf()

        item.save()

        if recursion_value > recursion_limit:
            return

        for link_item in links:
            movement = ModelDTO()
            movement.moveTo(item = link_item, 
                            db = db, 
                            recursion_value = recursion_value + 1,
                            recursion_limit = recursion_limit)
            item.LinkManager.link(link_item)

        return counts
