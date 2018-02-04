import os.path

from src.ram_module import Converter, DBUploader
from src.xml_module import Parser

#   Parsing xml to ram
scriptpath = os.path.dirname(__file__)

metadata_path = os.path.join(scriptpath, 'resources/prjadm.xdb.xml')
schema = Parser(metadata_path).parseXml2Ram()

#   Parsing ram to xml
xml = Converter().convertRam2Xml(schema)

#   Upload schema to sqlite database

config_path = os.path.join(scriptpath, 'db/sqlite_queries.cfg')
db_path = os.path.join(scriptpath, 'db/test_db.db')

dbUploader = DBUploader(config_path, db_path).upload(schema)


