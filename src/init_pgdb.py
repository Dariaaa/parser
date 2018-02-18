# Аргументом является XML, или DBD-файл.
# Результат - пустая БД под управлением PgSQL,
# структура которой определяется метаданными, переданными в качестве аргумента.
import argparse

from db import sqlite_queries
from dbd_module.dbd2ram import DBDownloader
from ram_module.ram2dbd_postgres import DBInitialisator
from xml_module.xml2ram import Parser

parser = argparse.ArgumentParser(description='CREATING EMPTY POSTGRESQL DATABASE')
parser.add_argument('--db', type=str, help="Path to db file")
parser.add_argument('--xml', type=str, help="Path to xml file")

args = parser.parse_args()

db = args.db
xml = args.xml

schemas = {}
db_name = ""

if xml:
    xml_parser = Parser(xml)
    schemas_from_xml = xml_parser.parseXml2Ram()
    schemas[0] = schemas_from_xml
    arr = xml.replace('.xml', '').split('\\')
    db_name = arr[arr.__len__() - 1]

elif db:
    db_downloader = DBDownloader(sqlite_queries,db,None)
    schemas_from_db = db_downloader.load()
    schemas=schemas_from_db
    arr = db.replace('.db','').split('\\')
    db_name = arr[arr.__len__()-1]

pg_init = DBInitialisator()
pg_init.create_database(db_name)

for schema in schemas.values():
    pg_init.create(schema)



