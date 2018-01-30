import unittest
import xml.dom.minidom as dom
from codecs import open as open
from src import Parser, Converter


class Test(unittest.TestCase):
    def test_parsing(self):
        """
            testing parsing xml -> ram -> xml
        """
        # creating new schema in ram
        schema = Parser("resources/tasks.xml").parseXml2Ram()
        # create xml file from schema
        xml = Converter().convertRam2Xml(schema)
        # writing result to file tasks1.xml
        file = open('resources/tasks1.xml', 'w', "utf8")
        xml.writexml(file, indent="  ", addindent="  ", newl='\n')
        file.close()
        diffs = ""
        # comparing 2 files - result and origin
        with open("resources/tasks.xml", 'r', 'utf8') as source_file, \
                open("resources/tasks1.xml", 'r', 'utf8') as result_file:
            equal = True
            i = 0
            for source_line in source_file:
                i += 1
                result_line = result_file.readline()
                if i == 1:
                    continue
                if source_line.split() != result_line.split():
                    diffs+='\norigin line {} : {} \nnew line {} : {}'.format(i, source_line, i, result_line)
                    equal = False

            if equal:
                print("Diffs not found. Files are equal.")

            source_file.close()
            result_file.close()

        self.assertTrue(equal, msg=diffs)
