import pprint
from xml.dom.minidom import parse, Element


class Reader:
    def __init__(self, filename):
        self.dom = parse(filename)
        self.tree = {}

