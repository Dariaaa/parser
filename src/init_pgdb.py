import argparse

import postgresql

from db import sqlite_queries
from db.config import result_path, postgressql_url
from dbd_module.dbd2ram import DBDownloader
from ram_module.ram2dbd_postgres import DBInitialisator
# from utils.writer import Writer
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

url = postgressql_url
conn = postgresql.open(url)

conn.execute('DROP DATABASE IF EXISTS ' + db_name)
conn.execute('CREATE DATABASE ' + db_name)
conn.close()
conn = postgresql.open(url + '/' + db_name.lower())


for schema in schemas.values():
    ddl = pg_init.generate_ddl(schema) # generate ddl instructions
    conn.execute(ddl)
    print("schema '{}' was created".format(schema.name))
    # Writer.write(result_path + db_name + ".ddl", ddl)

conn.close()




