import unittest
from codecs import open as open
from db import sqlite_queries
from db.config import test_result_path, resourses_path
from dbd_module import DBDownloader
from ram_module import DBUploader
from src.xml_module import Parser
from src.ram_module import Converter


class ParsingTest(unittest.TestCase):
    def test_parsing(self):

        """
            testing parsing xml -> ram -> xml
        """
        filename = "tasks.xml"
        resource = resourses_path + filename
        result = test_result_path + filename

        # creating new schema in ram
        schema = Parser(resource).parseXml2Ram()

        # create xml file from schema and writing result to file
        Converter().convertRam2Xml(schema,result)

        print("test_parsing result:")

        # comparing origin and result files
        diffs = self.compare(resource, result)

        # if diffs is empty then files are equal
        equal = True if diffs == "" else False

        if diffs == "":
            print("Diffs not found. Files are equal.")

        self.assertTrue(equal, msg=diffs)


    def test_downloading(self):
        """
                testing xml->ram->dbd->ram->xml
        """
        filename = "prjadm.xdb.xml"
        dbname = "prjadm.db"

        resource = resourses_path + filename
        result = test_result_path + filename
        result_db = test_result_path +  dbname

        #   Parsing xml to ram
        schema = Parser(resource).parseXml2Ram()

        #   Upload schema to sqlite database
        DBUploader(sqlite_queries, result_db).upload(schema)

        #   Download schemas from sqlite database
        schemas = DBDownloader(sqlite_queries, result_db,None).load()
        #   Get first schema
        Converter().convertRam2Xml(schemas[1],result)

        print("test_downloading result:")

        diffs = self.compare(resource, result)
        #   if diffs is empty then files are equal
        equal = True if diffs == "" else False

        if diffs == "":
            print("Diffs not found. Files are equal.")

        self.assertTrue(equal, msg=diffs)

    @staticmethod
    def compare(path1, path2):
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



            source_file.close()
            result_file.close()
            return diffs
