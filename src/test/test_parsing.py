import unittest
from codecs import open as open

from dbd_module import DBDownoader
from ram_module import DBUploader
from src.xml_module import Parser

import os

from src.ram_module import Converter


class ParsingTest(unittest.TestCase):
    def test_parsing(self):

        """
            testing parsing xml -> ram -> xml
        """
        ROOT_DIR = "D:/Projects/python/metadataparserpython/src/resources/";

        # creating new schema in ram
        schema = Parser(ROOT_DIR+"tasks.xml").parseXml2Ram()
        # create xml file from schema
        xml = Converter().convertRam2Xml(schema)
        # writing result to file parsing_test_result.xml
        self.write_file(xml, ROOT_DIR+'parsing_test_result.xml')
        # comparing origin and result files
        diffs = self.compare(ROOT_DIR+"tasks.xml", ROOT_DIR+'parsing_test_result.xml')
        # if diffs is empty then files are equal
        equal = True if diffs == "" else False
        self.assertTrue(equal, msg=diffs)

    def compare(self, path1, path2):
        """
        Find diffs between 2 files
        :param path1: file1 path
        :param path2: file2 path
        :return: diffs - lines where the files differ
        """
        diffs = ""
        with open(path1, 'r', 'utf8') as source_file, \
                open(path2, 'r', 'utf8') as result_file:

            i = 0
            for source_line in source_file:
                i += 1
                result_line = result_file.readline()
                if i == 1:
                    continue
                if source_line.split() != result_line.split():
                    diffs += '\norigin line {} : {} \nnew line {} : {}'.format(i, source_line, i, result_line)

            if diffs == "":
                print("Diffs not found. Files are equal.")

            source_file.close()
            result_file.close()
            return diffs

    def write_file(self, xml, path):
        """
        Write result to file
        :param xml: doc
        :param path: file path
        :return:
        """
        file = open(path, 'w', "utf8")
        xml.writexml(file, indent="  ", addindent="  ", newl='\n')
        file.close()

    def test_downloading(self):
        """
                testing xml->ram->dbd->ram->xml
        """
        ROOT = "D:/Projects/python/metadataparserpython/src/"
        RESOURCES_DIR = ROOT+"resources/"
        DB_DIR =  ROOT+"db/"

        config_path = DB_DIR+'sqlite_queries.cfg'
        db_path = DB_DIR+'test_db.db'

        metadata_path = RESOURCES_DIR+'prjadm.xdb.xml'

        #   Parsing xml to ram
        schema = Parser(metadata_path).parseXml2Ram()
        #   Parsing ram to xml
        xml = Converter().convertRam2Xml(schema)
        self.write_file(xml, RESOURCES_DIR+"xml2dbd_test_1.xml")
        # print(xml)
        # with open("resources/xml2dbd_result.xml", "w") as file:
        #    file.write(xml.toprettyxml(encoding="utf-8").decode("utf-8"))

        #   Upload schema to sqlite database
        DBUploader(config_path, db_path).upload(schema)

        schemas = DBDownoader(config_path, db_path).load()

        xml = Converter().convertRam2Xml(schemas[1])
        self.write_file(xml, RESOURCES_DIR+"xml2dbd_test_2.xml")
        diffs = self.compare(RESOURCES_DIR+"xml2dbd_test_1.xml",
                             RESOURCES_DIR+'xml2dbd_test_2.xml')
        # if diffs is empty then files are equal
        equal = True if diffs == "" else False

        self.assertTrue(equal, msg=diffs)
