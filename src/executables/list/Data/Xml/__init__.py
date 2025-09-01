from executables.templates.representations import Representation
from declarable.Arguments import StringArgument, ObjectArgument
import xmltodict

keys = {
    "xml.name": {
        "en_US": "Xml"
    }
}

class Implementation(Representation):
    docs = {
        "name": keys.get("xml.name"),
    }
