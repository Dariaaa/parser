from dbd_module import DBDownoader
from ram_module import Converter

# DOWNLOADING DATA FROM DBD TO XML

config_path = 'db/sqlite_queries.cfg'
db_path = 'db/test_db.db'

loader = DBDownoader(config_path, db_path)
schemas = loader.load()

xml = Converter().convertRam2Xml(schemas[1])
print(xml)
# with open("resources/dbd2xml_result.xml", "w") as file:
#    file.write(xml.toprettyxml(encoding="utf-8").decode("utf-8"))
