from db import DBInitialisator
from xml_module import Parser
import sys

# metadata_path = 'resources/prjadm.xdb.xml'
metadata_path = sys.argv[1]
db_name = sys.argv[2]

schema = Parser(metadata_path).parseXml2Ram()

dbInit = DBInitialisator()
dbInit.start(db_name, schema)
print("postgresql database "+db_name+" was created")


