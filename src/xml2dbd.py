from ram_module import Converter, DBUploader
from xml_module import Parser
import sys

# CONVERTING XML TO DBD

config_path = 'db/sqlite_queries.cfg'

db_path = sys.argv[1]
metadata_path = sys.argv[2]

#   Parsing xml to ram
schema = Parser(metadata_path).parseXml2Ram()

#   Parsing ram to xml
xml = Converter().convertRam2Xml(schema)

#   Upload schema to sqlite database
dbUploader = DBUploader(config_path, db_path).upload(schema)
print("database "+db_path+" was created")


