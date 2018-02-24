import argparse

import postgresql

from db import mssql_queries, sqlite_queries
from db.config import mssql_url, result_path, postgressql_url
from dbd_module.dbd2ram import DBDownloader
from dbd_module.mssql2ram import MSSQLDownloader
from ram_module.ram2dbd import DBUploader
from ram_module.ram2dbd_postgres import DBInitialisator
from data_transfering.data_transfering import DataTransfering
from ram_module.ram2xml import Converter
from utils.writer import Writer

parser = argparse.ArgumentParser(description='GENERATING DDL INSTRUCTIONS FOR CREATING EMPTY POSTGRESQL '
                                             'DB WHICH HAS INCOMING MSSQL DB STRUCTURE')

parser.add_argument('--db_name', type=str, help="Database name", default="dbo")
parser.add_argument('--db_path', type=str, help="Path for saved db files", default=result_path)
parser.add_argument('--ddl_path', type=str, help="Path for saved ddl instructions", default=result_path)
parser.add_argument('--mssql_url', type=str,help="Connection url",default=mssql_url)
parser.add_argument('--pg_url',type=str,default=postgressql_url)
args = parser.parse_args()

db_name = args.db_name
ddl_path = args.ddl_path
db_path = args.db_path
url_mssql = args.mssql_url
pg_url = args.pg_url

downloader = MSSQLDownloader(mssql_queries, url_mssql)
print("downloading db from " + url_mssql)
schema = downloader.load('dbo')
converter = Converter()
converter.convertRam2Xml(schema,result_path+'dbo.xml')

ddl_generator = DBInitialisator()
ddl = ddl_generator.generate_ddl(schema)
Writer.write(ddl_path + schema.name + ".ddl", '\n'.join(ddl))
print("ddl saved to {}".format(ddl_path + schema.name + ".ddl"))

pg_init = DBInitialisator()

conn = postgresql.open(pg_url)
conn.execute(pg_init.drop_database(db_name))
print("creating database {}".format(db_name))
conn.execute(pg_init.create_database_ddl(db_name))
conn.close()
print("connecting to database {}".format(db_name))
conn = postgresql.open(pg_url + '/' + db_name.lower())


conn.execute('\n '.join(ddl))

data_transfer = DataTransfering(db_name, mssql_url, pg_url + '/' + db_name.lower())

schemas = {}
schemas[0] = schema
print("start data transferring")
data_transfer.start(schemas)
