from Plugins.App.Storage.Storage import app

class ModelDTO:
    MOVE_TYPE_TRANSFER = "move"
    MOVE_TYPE_COPY = "copy"

    def moveTo(self,
               item, 
               db_wrapper,
               recursion_value: int = 0,
               recursion_limit: int = 10,
               storage_units_move_storage = None,
               storage_units_move_type = "move"
               ):
        counts = 0
        links = []

        if getattr(item, "LinkManager", None) != None:
            relations = item.LinkManager.getRelations()

            app.logger.log(f"Found {len(relations)} linked at {item.name_db_id}", section=["Saveable"])

            for link_item in relations:
                links.append(link_item.getStructure())

        with db_wrapper.db_ref.bind_ctx([item]):
            item.setWrapper(db_wrapper)

            app.logger.log(f"Set db of item {item.name_db_id} to {db_wrapper.db_name}", section=["Saveable", "DB"])

            if item.self_name == "StorageUnit":
                if storage_units_move_storage != None:
                    match(storage_units_move_type):
                        case ModelDTO.MOVE_TYPE_TRANSFER:
                            item.moveSelf(storage_units_move_storage)
                        case ModelDTO.MOVE_TYPE_COPY:
                            item.copySelf(storage_units_move_storage)

            item.save()

            if recursion_value > recursion_limit:
                return item

            for link_obj in links:
                link_item = link_obj.get("item")
                link_type = link_obj.get("type")

                movement = ModelDTO()
                new_item = movement.moveTo(item = link_item, 
                                db_wrapper = db_wrapper, 
                                recursion_value = recursion_value + 1,
                                recursion_limit = recursion_limit,
                                storage_units_move_storage = storage_units_move_storage,
                                storage_units_move_type = storage_units_move_type)
                item.LinkManager.relations.setWrapper(db_wrapper)
                item.LinkManager.link(new_item, link_type)

        return item
