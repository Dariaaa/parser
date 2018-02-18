import argparse
from db import mssql_queries, sqlite_queries
from db.config import mssql_url, result_path
from dbd_module.dbd2ram import DBDownloader
from ram_module.ram2dbd import DBUploader
from ram_module.ram2dbd_postgres import DBInitialisator
from utils.writer import Writer

parser = argparse.ArgumentParser(description='GENERATING DDL INSTRUCTIONS FOR CREATING EMPTY POSTGRESQL '
                                             'DB WHICH HAS INCOMING MSSQL DB STRUCTURE')

parser.add_argument('--db_name', type=str, help="Database name", default="Northwind")
parser.add_argument('--db_path', type=str, help="Path for saved db files", default=result_path)
parser.add_argument('--ddl_path', type=str, help="Path for saved ddl instructions", default=result_path)
parser.add_argument('--mssql_url', type=str,help="Connection url",default=mssql_url)

args = parser.parse_args()

db_name = args.db_name
ddl_path = args.ddl_path
db_path = args.db_path
url_mssql = args.mssql_url

downloader = DBDownloader(mssql_queries, None, url_mssql)
schemas = downloader.load()

ddl_generator = DBInitialisator()

uploader = DBUploader(sqlite_queries,db_path + db_name)

for schema in schemas.values():
    if len(schema.tables)>0:
        #   generate ddl instructions and save
        ddl = ddl_generator.generate_ddl(schema)
        Writer.write(ddl_path + schema.name + ".ddl", ddl)
        #   upload schema to sqlite database
        uploader.upload(schema)

