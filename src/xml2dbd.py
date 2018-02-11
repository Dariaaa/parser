from db import sqlite_queries
from ram_module import DBUploader
from xml_module import Parser
import sys

# CONVERTING XML TO DBD

db_path = sys.argv[1]
metadata_path = sys.argv[2]

#   Parsing xml to ram
parser = Parser(metadata_path)
schema = parser.parseXml2Ram()

#   Upload schema to sqlite database
uploader = DBUploader(sqlite_queries, db_path)
uploader.upload(schema)

print("database "+db_path+" was created")


