import xml.dom.minidom as dom

from src import (xml2ram)

#   Reading xml file using minidom
xml = dom.parse("resources/tasks.xml")

#   Parsing xml to ram
schema = xml2ram(xml)

