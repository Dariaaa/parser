from db import sqlite_queries
from dbd_module import DBDownloader
from ram_module import Converter
import sys

# DOWNLOADING DATA FROM DBD TO XML

db_path = sys.argv[1]
xml_path = sys.argv[2]

#   downloading schemas from sqlite database
loader = DBDownloader(sqlite_queries, db_path, None)
schemas = loader.load()

#   converting from ram representation to xml file
converter = Converter()
converter.convertRam2Xml(schemas[1],xml_path)

print("file "+xml_path+" was created")
