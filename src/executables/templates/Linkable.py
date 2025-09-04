from app.App import logger
from db.LinkManager import LinkManager

class Linkable:
    def addLink(self, item):
        if getattr(self, "linking_queue", None) == None:
            self.linking_queue = []

        self.linking_queue.append(item)

    def doLink(self, link_item):
        if getattr(self, "linking_queue", None) == None:
            self.linking_queue = []

        for item in self.linking_queue:
            link_manager = LinkManager(item)

            try:
                link_manager.link(item, link_item)
            except AssertionError as _e:
                logger.logException(_e, section=logger.SECTION_LINKAGE)
