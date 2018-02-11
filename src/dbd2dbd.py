from db import mssql_url, mssql_queries
from db.config import result_path
from dbd_module import DBDownloader
from ram_module import Converter, DBInitialisator
from utils import ItemNotFoundException

db_name = "Northwind"

#   download data from mssql database
downloader = DBDownloader(mssql_queries, None, mssql_url)
schemas = downloader.load()

#   write result to xml file for checking
converter  = Converter()
for schema in schemas.values():
    try:
        converter.convertRam2Xml(schema,result_path + schema.name + ".xml")
    except ItemNotFoundException:
        pass

#   create empty postgresql database
init = DBInitialisator()
init.start(db_name, schemas[1])

print("postgresql database " + db_name + " was created")
