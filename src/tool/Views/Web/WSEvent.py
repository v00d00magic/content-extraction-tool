from Utils.Wrap import Wrap
from typing import List

class WSEventEnum():
    EVENT_LOG = "log"
    EVENT_CALL = "call"

class WSEvent(Wrap):
    type: List = "none"
    index: int = 0
    payload: dict = {}

    def getStructure(self):
        return {
            "type": self.type,
            "index": self.index,
            "payload": self.payload
        }
