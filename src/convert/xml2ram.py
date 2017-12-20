from src.model import Domain, Table, Field, Index, Constraint, Schema

__all__ = ["xml2ram"]


def xml2ram(xml):
    """

    Parsing xml to ram

    :param xml: xml.dom.minidom.Document
    :return: Schema
    """
    schema = _parseSchema(xml)
    schema.domains = _parseDomains(xml)
    schema.tables = _parseTables(xml)

    return schema


def _parseSchema(xml):
    """

    Create schema from xml

    :param xml: xml.dom.minidom.Document
    :return: Schema
    """
    schema = Schema()
    attributes = xml.documentElement.attributes.items()
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
                raise ValueError("In tag \"{}\" invalid attribute name \"{}\"".format(schema.nodeName, name))
    return schema

def _parseDomains(xml):
    """

    Create list of domains (objects Domain)

    :param xml: xml.dom.minidom.Document
    :return:
    """
    list = []
    domain_parent = xml.getElementsByTagName("domain")
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
                domain.align = val
            elif name.lower() == "length":
                domain.width = val
            elif name.lower() == "scale":
                domain.precision = val
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
                        raise ValueError("Invalid format of propertiess: {}".format(val))
        list.append(domain)
    return list


def _parseTables(xml):
    """
    Create list of object Table

    Args:
        xml : xml.dom.minidom.Document

    Return: list<Table>

    """
    list = []
    xml_tables = xml.getElementsByTagName("table")
    for item in xml_tables:
        table = _parseTable(item)
        table.fields = _parseFields(item)
        table.indexes = _parseIndexes(item)
        table.constraints = _parseConstraints(item)
        list.append(table)

    return list

def _parseTable(item):
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
                    raise ValueError("Invalid format of properties: {}".format(val))
        elif name.lower() == "ht_table_flags":
            table.ht_table_flags = val
        elif name.lower() == "access_level":
            table.access_level = val
        else:
            raise ValueError("In tag {} invalid attribute name \"{}\"".format(table.nodeName, name))
    return table


def _parseFields(xml):
    """

    Create list of fields (objects Field)

    :param xml:
    :return:
    """
    if xml.nodeName != "table":
        raise TypeError("Element is not a table")

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
                        raise ValueError("Invalid format of properties: {}".format(val))
            elif name.lower() == "description":
                field.descr = val
            else:
                raise ValueError("In tag \"{}\" invalid attribute name \"{}\"".format(field.nodeName, name))

        list.append(field)

    return list


def _parseIndexes(xml):
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
                pass
            elif name.lower() == "props":
                for prop in val.split(", "):
                    if prop == "fulltext":
                        tmp.fulltext = True
                    elif prop == "uniqueness":
                        tmp.uniqueness = True
                    else:
                        raise ValueError("Invalid format of props string: {}".format(val))
            else:
                raise ValueError("In tag \"{}\" invalid attribute name \"{}\"".format(item.nodeName, name))
        list.append(tmp)
    return list

def _parseConstraints(xml):
    """

    Create list of constraint (objects Constraint)

    :param xml:
    :return:
    """
    if xml.nodeName != "table":
        raise TypeError("Element is not a table")

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
                constraint.items = val
            elif name.lower() == "props":
                for prop in val.split(", "):
                    if prop == "has_value_edit":
                        constraint.has_value_edit = True
                    elif prop == "cascading_delete":
                        constraint.cascading_delete = True
                    elif prop == "full_cascading_delete":
                        constraint.full_cascading_delete = True
                    else:
                        raise ValueError("Invalid format of props string: {}".format(val))
            elif name.lower() == "reference_type":
                constraint.reference_type = val
            elif name.lower() == "reference":
                constraint.reference = val
            else:
                raise ValueError("In tag \"{}\" invalid attribute name \"{}\"".format(constraint.nodeName, name))
        list.append(constraint)
    return list