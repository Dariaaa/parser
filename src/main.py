from src import (Parser,
                 Converter,
                 DBUploader)

#   Parsing xml to ram
schema = Parser("resources/prjadm.xdb.xml").parseXml2Ram()

#   Parsing ram to xml
xml = Converter().convertRam2Xml(schema)

#   Upload schema to sqlite database
dbUploader = DBUploader("test_db.db").upload(schema)


