import argparse

import postgresql

from db import sqlite_queries
from db.config import postgressql_url, result_path
from dbd_module.dbd2ram import DBDownloader
from ram_module.ram2dbd_postgres import DBInitialisator
# from utils.writer import Writer
from utils.writer import Writer
from xml_module.xml2ram import Parser

parser = argparse.ArgumentParser(description='CREATING EMPTY POSTGRESQL DATABASE')
parser.add_argument('--db', type=str, help="Path to db file")
parser.add_argument('--xml', type=str, help="Path to xml file")
parser.add_argument('--ddl_path',type=str, help="Path to saved ddl instructions",default=result_path)
args = parser.parse_args()

db = args.db
xml = args.xml
ddl_path = args.ddl_path

schemas = {}
db_name = ""

if xml:
    print("reading file {} ".format(xml))
    xml_parser = Parser(xml)
    schemas_from_xml = xml_parser.parseXml2Ram()
    schemas[0] = schemas_from_xml
    arr = xml.replace('.xml', '').split('\\')
    db_name = arr[arr.__len__() - 1]

elif db:
    print("reading database {} ".format(db))
    db_downloader = DBDownloader(sqlite_queries,db,None)
    schemas_from_db = db_downloader.load()
    schemas=schemas_from_db
    arr = db.replace('.db','').split('\\')
    db_name = arr[arr.__len__()-1]

pg_init = DBInitialisator()

print("establishing connection...")
url = postgressql_url
conn = postgresql.open(url)
conn.execute(pg_init.drop_database(db_name))
print("creating database {}".format(db_name))
conn.execute(pg_init.create_database_ddl(db_name))
conn.close()
print("connecting to database {}".format(db_name))
conn = postgresql.open(url + '/' + db_name.lower())


for schema in schemas.values():
    print("generating ddl for schema {}".format(schema.name))
    ddl = pg_init.generate_ddl(schema, True) # generate ddl instructions
    Writer.write(ddl_path + db_name + ".ddl", '\n '.join(ddl))
    print("ddl saved to {}".format(ddl_path + db_name + ".ddl"))
    conn.execute('\n '.join(ddl))
    print("schema '{}' was created".format(schema.name))

conn.close()




