from ram_module import Converter, DBUploader
from xml_module import Parser

# CONVERTING XML TO DBD

config_path = 'db/sqlite_queries.cfg'
db_path = 'db/test_db.db'
metadata_path = 'resources/prjadm.xdb.xml'

#   Parsing xml to ram
schema = Parser(metadata_path).parseXml2Ram()
#   Parsing ram to xml
xml = Converter().convertRam2Xml(schema)
# print(xml)
# with open("resources/xml2dbd_result.xml", "w") as file:
#    file.write(xml.toprettyxml(encoding="utf-8").decode("utf-8"))

#   Upload schema to sqlite database
dbUploader = DBUploader(config_path, db_path).upload(schema)


