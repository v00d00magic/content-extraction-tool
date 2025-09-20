class ModelDTO:
    def moveTo(self, 
               item, 
               db,
               recursion_value = 0,
               recursion_limit = 10):
        counts = 0
        item.setDb(db)
        if hasattr(item, "moveSelf") == True:
            item.moveSelf()

        item.save()

        if recursion_value > recursion_limit:
            return

        if getattr(item, "Links", None) != None:
            links = item.Links.getLinkedList()
            for link_item in links:
                movement = ModelDTO()
                movement.moveTo(item = link_item, 
                                db = db, 
                                recursion_value = recursion_value + 1,
                                recursion_limit = recursion_limit)
                item.Links.link(link_item)

        return counts
