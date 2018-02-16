import argparse
from db import sqlite_queries
from ram_module.ram2dbd import DBUploader
from xml_module.xml2ram import Parser
# import sys

# CONVERTING XML TO DBD

parser = argparse.ArgumentParser(description='DOWNLOADING DATA FROM DBD TO XML')
parser.add_argument('--db', type=str, help="Path to db file")
parser.add_argument('--xml', type=str, help="Path to xml file")

arguments = parser.parse_args()

db_path = arguments.db
metadata_path = arguments.xml

#   Parsing xml to ram
parser = Parser(metadata_path)
schema = parser.parseXml2Ram()

#   Upload schema to sqlite database
uploader = DBUploader(sqlite_queries, db_path)
uploader.upload(schema)

print("database "+db_path+" was created")


