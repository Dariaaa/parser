import argparse
from db import sqlite_queries
from dbd_module.dbd2ram import DBDownloader
from ram_module.ram2xml import Converter

# DOWNLOADING DATA FROM DBD TO XML

parser = argparse.ArgumentParser(description='DOWNLOADING DATA FROM DBD TO XML')
parser.add_argument('--db', type=str, help="Path to db file")
parser.add_argument('--xml', type=str, help="Path to xml file")

arguments = parser.parse_args()

db_path = arguments.db
xml_path = arguments.xml

#   downloading schemas from sqlite database
loader = DBDownloader(sqlite_queries, db_path, None)
schemas = loader.load()

#   converting from ram representation to xml file
converter = Converter()
converter.convertRam2Xml(schemas[1],xml_path)

print("file "+xml_path+" was created")
