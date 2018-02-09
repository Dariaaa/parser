from dbd_module import DBDownoader
from ram_module import Converter
import sys
from codecs import open as open

# DOWNLOADING DATA FROM DBD TO XML

config_path = 'db/sqlite_queries.cfg'
# db_path = 'db/test_db.db'
db_path = sys.argv[1]
xml_path = sys.argv[2]

# db_path = 'D:\\Projects\\python\\metadataparserpython\\src\\db\\test_db.db'

loader = DBDownoader(config_path, db_path)
schemas = loader.load()

xml = Converter().convertRam2Xml(schemas[1])
file = open(xml_path, 'w', "utf8")
xml.writexml(file, indent="  ", addindent="  ", newl='\n')
file.close()
print("file "+xml_path+" was created")


# print(xml)
# with open("resources/dbd2xml_result.xml", "w") as file:
#    file.write(xml.toprettyxml(encoding="utf-8").decode("utf-8"))
