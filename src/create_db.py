from db import DBInitialisator
from xml_module import Parser

metadata_path = 'resources/prjadm.xdb.xml'

schema = Parser(metadata_path).parseXml2Ram()

dbInit = DBInitialisator()
dbInit.start('test1', schema)

