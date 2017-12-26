import xml.dom.minidom as dom

from src import (xml2ram,
                 ram2xml)
# import io

#   Reading xml file using minidom
xml = dom.parse("resources/tasks.xml")

#   Parsing xml to ram
schema = xml2ram(xml)

#   Parsing ram to xml
xml = ram2xml(schema)

# print(xml.toprettyxml(indent="  ", encoding="utf-8").decode("utf-8"))
