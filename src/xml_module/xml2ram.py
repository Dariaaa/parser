import xml.dom.minidom as dom

from src.ram_module import Domain, Table, Field, Index, Constraint, Schema, ConstraintDetail, IndexDetail
from src.utils import ParseError


class Parser:
    """
    Create Ram representation from xml file
    """
    def __init__(self, xml_file_path):
        self.xml = dom.parse(xml_file_path)

    def parseXml2Ram(self):
        """
        Parse xml to ram
        :return:
        """
        schema = self._parseSchema()
        schema.domains = self._parseDomains()
        schema.tables = self._parseTables()

        return schema


    def _parseSchema(self):
        """
        Create schema from xml
        :param xml: xml.dom.minidom.Document
        :return: Schema
        """
        schema = Schema()
        attributes = self.xml.documentElement.attributes.items()
        for name, val in attributes:
                if name.lower() == "name":
                        schema.name = val
                elif name.lower() == "version":
                        schema.version = val
                elif name.lower() == "fulltext_engine":
                    schema.fulltext_engine = val
                elif name.lower() == "description":
                    schema.descr = val
                else:
                    raise ParseError("In tag \"{}\" invalid attribute name \"{}\"".format(schema.nodeName, name),"_parseSchema")
        return schema

    def _parseDomains(self):
        """

        Create list of domains (objects Domain)

        :param xml: xml.dom.minidom.Document
        :return:
        """
        list = []
        domain_parent = self.xml.getElementsByTagName("domain")
        for item in domain_parent:
            domain = Domain()
            attributes = item.attributes.items()
            for name, val in attributes:
                if name.lower() == "name":
                    domain.name = val
                elif name.lower() == "description":
                    domain.descr = val
                elif name.lower() == "type":
                    domain.type = val
                elif name.lower() == "align":
                    domain.align = val
                elif name.lower() == "width":
                    domain.width = val
                elif name.lower() == "precision":
                    domain.precision = val
                elif name.lower() == "char_length":
                    domain.char_length = val
                elif name.lower() == "length":
                    domain.length = val
                elif name.lower() == "scale":
                    domain.scale = val
                elif name.lower() == "props":
                    for prop in val.split(", "):
                        if prop == "show_null":
                            domain.show_null = True
                        elif prop == "summable":
                            domain.summable = True
                        elif prop == "case_sensitive":
                            domain.case_sensitive = True
                        elif prop == "show_lead_nulls":
                            domain.show_lead_nulls = True
                        elif prop == "thousands_separator":
                            domain.thousands_separator = True
                        else:
                            raise ParseError("Invalid format of propertiess: {}".format(val),"_parseDomains")
            list.append(domain)
        return list


    def _parseTables(self):
        """
        Create list of object Table

        Args:
            xml : xml.dom.minidom.Document

        Return: list<Table>

        """
        list = []
        xml_tables = self.xml.getElementsByTagName("table")
        for item in xml_tables:
            table = self._parseTable(item)
            table.fields = self._parseFields(item)
            table.indexes = self._parseIndexes(item)
            table.constraints = self._parseConstraints(item)
            list.append(table)

        return list

    def _parseTable(self,item):
        """

        Parse table from xml

        :param xml: xml.dom.minidom.Document
        :return:
        """

        table = Table()
        attributes = item.attributes.items()
        for name, val in attributes:
            if name.lower() == "name":
                table.name = val
            elif name.lower() == "description":
                table.descr = val
            elif name.lower() == "props":
                for prop in val.split(", "):
                    if prop == "add":
                        table.add = True
                    elif prop == "edit":
                        table.edit = True
                    elif prop == "delete":
                        table.delete = True
                    else:
                        raise ParseError("Invalid format of properties: {}".format(val),"_parseTable")
        return table


    def _parseFields(self, xml):
        """

        Create list of fields (objects Field)

        :param xml:
        :return:
        """
        if xml.nodeName != "table":
            raise ParseError("Element is not a table","_parseFields")

        list = []
        xml_fields = xml.getElementsByTagName("field")
        for item in xml_fields:
            field = Field()
            attributes = item.attributes.items()
            for name, val in attributes:
                if name.lower() == "name":
                    field.name = val
                elif name.lower() == "rname":
                    field.rname = val
                elif name.lower() == "domain":
                    field.domain = val
                elif name.lower() == "props":
                    for prop in val.split(", "):
                        if prop == "input":
                            field.input = True
                        elif prop == "edit":
                            field.edit = True
                        elif prop == "show_in_grid":
                            field.show_in_grid = True
                        elif prop == "show_in_details":
                            field.show_in_details = True
                        elif prop == "is_mean":
                            field.is_mean = True
                        elif prop == "autocalculated":
                            field.autocalculated = True
                        elif prop == "required":
                            field.required = True
                        else:
                            raise ParseError("Invalid format of properties: {}".format(val),"_parseFields")
                elif name.lower() == "description":
                    field.descr = val
                else:
                    raise ParseError("In tag \"{}\" invalid attribute name \"{}\"".format(field.nodeName, name),"_parseFields")

            list.append(field)

        return list


    def _parseIndexes(self, xml):
        """

        Create list of indexes (object Index)

        :param xml:
        :return:
        """
        if xml.nodeName != "table":
            raise TypeError("Element is not a table")

        list = []
        xml_indexes = xml.getElementsByTagName("index")
        for item in xml_indexes:
            tmp = Index()

            attributes = item.attributes.items()
            for name, val in attributes:
                if name.lower() == "field":
                    detail = IndexDetail()
                    detail.value = val
                    tmp.details.append(detail)

                elif name.lower() == "props":
                    for prop in val.split(", "):
                        if prop == 'local':
                            tmp.local = True
                        if prop == "fulltext":
                            tmp.kind = "fulltext"
                        elif prop == "uniqueness":
                            tmp.kind = "uniqueness"
                        else:
                            raise ParseError("Invalid format of props string: {}".format(val), "_parseIndexes")
                else:
                    raise ParseError("In tag \"{}\" invalid attribute name \"{}\"".format(item.nodeName, name), "_parseIndexes")


            for detail_node in item.childNodes:
                if detail_node.tagName != 'item':
                    raise Exception()
                detail = self._create_index_detail(detail_node._attrs)
                tmp.details.append(detail)
            list.append(tmp)
        return list

    def _parseConstraints(self, xml):
        """

        Create list of constraint (objects Constraint)

        :param xml:
        :return:
        """
        if xml.nodeName != "table":
            raise ParseError("Element is not a table","_parseConstraints")

        list = []
        xmlConstraints = xml.getElementsByTagName("constraint")
        for item in xmlConstraints:
            constraint = Constraint()
            attributes = item.attributes.items()
            for name, val in attributes:
                if name.lower() == "name":
                    constraint.name = val
                elif name.lower() == "kind":
                    constraint.kind = val
                elif name.lower() == "items":
                    detail = ConstraintDetail()
                    detail.value = val
                    constraint.details.append(detail)
                elif name.lower() == "props":
                    for prop in val.split(", "):
                        if prop == "has_value_edit":
                            constraint.has_value_edit = True
                        elif prop == "cascading_delete":
                            constraint.cascading_delete = False
                        elif prop == "full_cascading_delete":
                            constraint.cascading_delete = True
                        else:
                            raise ParseError("Invalid format of props string: {}".format(val),"_parseConstraints")
                elif name.lower() == "reference":
                    constraint.reference = val
                elif name.lower() == 'expression':
                    constraint.expression = val
                else:
                    raise ParseError("In tag \"{}\" invalid attribute name \"{}\"".format(constraint.nodeName, name),"_parseConstraints")
            list.append(constraint)

            for detail_node in item.childNodes:
                if detail_node.tagName != 'item':
                    raise Exception()
                detail = self._create_constraint_detail(detail_node._attrs)
                constraint.details.append(detail)

        return list

    def _create_constraint_detail(self, attr_dict):

        detail = ConstraintDetail()
        for attr, val in attr_dict:
            if attr == 'value':
                detail.value = val
            else:
                pass
        return detail

    def _create_index_detail(self, attr_dict):

        detail = IndexDetail()
        for attr, val in attr_dict:
            if attr == 'value':
                detail.value = val
            elif attr == 'expression':
                detail.expression = val
            elif attr == 'descend':
                detail.descend = val
            else:
                pass
        return detail

