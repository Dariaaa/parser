from src import (Parser,
                 Converter,
                 DBUploader)

#   Parsing xml to ram
schema = Parser("resources/prjadm.xdb.xml").parseXml2Ram()

#   Parsing ram to xml
xml = Converter().convertRam2Xml(schema)
with open("result.xml", "w") as file:
   file.write(xml.toprettyxml(encoding="utf-8").decode("utf-8"))

#   Upload schema to sqlite database
dbUploader = DBUploader("resources/sql/sqlite_queries.cfg", "test_db.db").upload(schema)


