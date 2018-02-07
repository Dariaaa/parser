from db.postgres_db_init import DBInitialisator
from src.xml_module import Parser

metadata_path = 'resources/prjadm.xdb.xml'

schema = Parser(metadata_path).parseXml2Ram()

dbInit = DBInitialisator()
dbInit.start('test1', schema)

