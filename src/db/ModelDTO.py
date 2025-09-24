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
            relations = item.LinkManager.getItemsAndTypes()

            logger.log(f"Found {len(relations)} linked at {item.name_db_id}", section=["Saveable"])

            for link_item in relations:
                links.append(link_item)

        item.setDb(db)

        logger.log(f"Set db of item {item.name_db_id} to {item.getDbName()}", section=["Saveable", "DB"])

        if hasattr(item, "moveSelf") == True:
            item.moveSelf()

        item.save()

        if recursion_value > recursion_limit:
            return

        for link_item in links:
            so_item_to_link = link_item.get("item")
            movement = ModelDTO()
            movement.moveTo(item = so_item_to_link, 
                            db = db, 
                            recursion_value = recursion_value + 1,
                            recursion_limit = recursion_limit)
            item.LinkManager.link(so_item_to_link, link_item.get("type"))

        return counts
