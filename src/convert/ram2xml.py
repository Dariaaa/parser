from src import minidom_fixed as dom
from src.exceptions import ParseError

__all__ = ["ram2xml"]


def ram2xml(schema):
    if schema is None:
        raise ParseError("Schema is none", "ram2xml")

    xml = dom.Document()

    node = xml.createElement("dbd_schema")

    if schema.fulltext_engine is not None:
        node.setAttribute("fulltext_engine", schema.fulltext_engine)
    if schema.version is not None:
        node.setAttribute("version", schema.version)
    if schema.name is not None:
        node.setAttribute("name", schema.name)
    if schema.descr is not None:
        node.setAttribute("description", schema.descr)
    node.appendChild(xml.createElement("custom"))

    domains = xml.createElement("domains")
    for domain in create_domain(xml, schema.domains):
        domains.appendChild(domain)
    node.appendChild(domains)

    tables = xml.createElement("tables")
    for table in create_table(xml, schema.tables):
        tables.appendChild(table)
    node.appendChild(tables)

    xml.appendChild(node)
    return xml


def create_domain(xml, domains):

    for domain in domains:
        node = xml.createElement("domain")
        if domain.name is not None:
            node.setAttribute("name", domain.name)
        if domain.descr is not None:
            node.setAttribute("description", domain.descr)
        if domain.type is not None:
            node.setAttribute("type", domain.type)
        if domain.align is not None:
            node.setAttribute("align", domain.align)
        if domain.width is not None:
            node.setAttribute("width", domain.width)
        if domain.length is not None:
            node.setAttribute("length", domain.length)
        if domain.precision is not None:
            node.setAttribute("precision", domain.precision)

        properties = []
        if domain.show_null:
            properties.append("show_null")
        if domain.summable:
            properties.append("summable")
        if domain.case_sensitive:
            properties.append("case_sensitive")
        if domain.show_lead_nulls:
            properties.append("show_lead_nulls")
        if domain.thousands_separator:
            properties.append("thousands_separator")

        if len(properties) != 0:
            node.setAttribute("props", ", ".join(properties))

        if domain.char_length is not None:
            node.setAttribute("char_length", domain.char_length)
        if domain.length is not None:
            node.setAttribute("length", domain.length)
        if domain.scale is not None:
            node.setAttribute("scale", domain.scale)
        yield node


def create_table(xml, tables):

    for table in tables:
        node = xml.createElement("table")
        if table.name is not None:
            node.setAttribute("name", table.name)
        if table.descr is not None:
            node.setAttribute("description", table.descr)

        properties = []
        if table.add:
            properties.append("add")
        if table.edit:
            properties.append("edit")
        if table.delete:
            properties.append("delete")

        if len(properties) != 0:
            node.setAttribute("props", ", ".join(properties))

        if table.ht_table_flags is not None:
            node.setAttribute("ht_table_flags", table.ht_table_flags)
        if table.access_level is not None:
            node.setAttribute("access_level", table.access_level)

        if len(table.fields) != 0:
            for field in create_field(xml, table.fields):
                node.appendChild(field)

        if len(table.constraints) != 0:
            for constraint in create_constraint(xml, table.constraints):
                node.appendChild(constraint)

        if len(table.indexes) != 0:
            for index in create_index(xml, table.indexes):
                node.appendChild(index)

        yield node


def create_field(xml, fields):
    for field in fields:
        node = xml.createElement("field")
        if field.name is not None:
            node.setAttribute("name", field.name)
        if field.rname is not None:
            node.setAttribute("rname", field.rname)
        if field.domain is not None:
            node.setAttribute("domain", field.domain)
        if field.descr is not None:
            node.setAttribute("description", field.descr)

        properties = []
        if field.input:
            properties.append("input")
        if field.edit:
            properties.append("edit")
        if field.show_in_grid:
            properties.append("show_in_grid")
        if field.show_in_details:
            properties.append("show_in_details")
        if field.is_mean:
            properties.append("is_mean")
        if field.autocalculated:
            properties.append("autocalculated")
        if field.required:
            properties.append("required")

        if len(properties) != 0:
            node.setAttribute("props", ", ".join(properties))

        yield node


def create_constraint(xml, constraints):

    for constraint in constraints:
        node = xml.createElement("constraint")
        if constraint.name is not None:
            node.setAttribute("name", constraint.name)
        if constraint.kind is not None:
            node.setAttribute("kind", constraint.kind)
        if constraint.items is not None:
            node.setAttribute("items", constraint.items)
        if constraint.reference_type is not None:
            node.setAttribute("reference_type", constraint.reference_type)
        if constraint.reference is not None:
            node.setAttribute("reference", constraint.reference)
        properties = []
        if constraint.has_value_edit:
            properties.append("has_value_edit")
        if constraint.cascading_delete:
            properties.append("cascading_delete")
        if constraint.full_cascading_delete:
            properties.append("full_cascading_delete")

        if len(properties) != 0:
            node.setAttribute("props", ", ".join(properties))
        yield node


def create_index(xml, indexes):

    for index in indexes:
        if len(index.fields) != 0:
            node = xml.createElement("index")
            if len(index.fields) == 1:
                node.setAttribute("field", index.fields[0])
            else:
                # когда в индекс входит больше одного поля
                pass
            if index.name is not None:
                node.setAttribute("name", index.name)
            properties = []
            if index.fulltext:
                properties.append("fulltext")
            if index.uniqueness:
                properties.append("uniqueness")
            if len(properties) != 0:
                node.setAttribute("props", ", ".join(properties))

            yield node
        else:
            raise ParseError("Error! Index does not contain fields", "_create_index")


