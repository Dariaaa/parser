from src import minidom_fixed as dom
from src.exceptions import ParseError


class Converter:
    def __init__(self):
        self.xml = dom.Document()


    def create_schema(self, schema):
        """
        Create nodes "dbd_schema" from Schema object
        :param schema: Schema
        :return:
        """
        node = self.xml.createElement("dbd_schema")

        if schema.fulltext_engine is not None:
            node.setAttribute("fulltext_engine", schema.fulltext_engine)
        if schema.version is not None:
            node.setAttribute("version", schema.version)
        if schema.name is not None:
            node.setAttribute("name", schema.name)
        if schema.descr is not None:
            node.setAttribute("description", schema.descr)
        node.appendChild(self.xml.createElement("custom"))
        return node


    def create_domain(self, domains):
        """
        Create nodes "domain" from list of Domain objects
        :param domains: Domain
        :return:
        """
        for domain in domains:
            node = self.xml.createElement("domain")
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


    def create_table(self, tables):
        """
        Create nodes "table" from list of Table objects
        :param tables: Table
        :return:
        """
        for table in tables:
            node = self.xml.createElement("table")
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

            if len(table.fields) != 0:
                for field in self.create_field(table.fields):
                    node.appendChild(field)

            if len(table.constraints) != 0:
                for constraint in self.create_constraint(table.constraints):
                    node.appendChild(constraint)

            if len(table.indexes) != 0:
                for index in self.create_index(table.indexes):
                    node.appendChild(index)

            yield node


    def create_field(self, fields):
        """
        Create nodes "field" from list of Field objeccts
        :param fields: Field
        :return:
        """
        for field in fields:
            node = self.xml.createElement("field")
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


    def create_constraint(self, constraints):
        """
        Create nodes "constraint" from list of Constraint objects
        :param constraints: Constraint
        :return:
        """
        for constraint in constraints:
            node = self.xml.createElement("constraint")
            if constraint.name is not None:
                node.setAttribute("name", constraint.name)
            if constraint.kind is not None:
                node.setAttribute("kind", constraint.kind)
            if len(constraint.details) == 1:
                node.setAttribute("items", constraint.details[0].value)
            # if constraint.reference_type is not None:
            #     node.setAttribute("reference_type", constraint.reference_type)
            if constraint.reference is not None:
                node.setAttribute("reference", constraint.reference)
            if constraint.expression is not None:
                node.setAttribute('expression', constraint.expression)

            properties = []
            if constraint.has_value_edit:
                properties.append("has_value_edit")
            if constraint.cascading_delete:
                properties.append("cascading_delete")
            if constraint.full_cascading_delete:
                properties.append("full_cascading_delete")

            if len(properties) != 0:
                node.setAttribute("props", ", ".join(properties))

            # for detail in constraint.details:
            #     detail_output = self._create_constraint_detail_dom(detail)
            #     node.appendChild(detail_output)

            yield node


    def create_index(self, indexes):
        """
        Create nodes "index" from list of Index objects
        :param indexes: Index
        :return:
        """
        nodes = []
        for index in indexes:
            node = self.xml.createElement("index")

            if index.name:
                node.setAttribute('name', index.name)
            if len(index.details) == 1:
                node.setAttribute('field', index.details[0].value)
            props = []

            if index.local:
                props.append('local')
            if index.kind == 'uniqueness':
                props.append('uniqueness')
            if index.kind == 'fulltext':
                props.append('fulltext')
            if len(props) > 0:
                node.setAttribute('props', ', '.join(props))

            # for detail in index.details:
            #     detail_output = self._create_index_detail_dom(detail)
            #     node.appendChild(detail_output)
            nodes.append(node)
        return nodes


    def convertRam2Xml(self, schema):
        """
        Create ram representation of incoming Schema object
        :param schema: Schema
        :return:
        """
        if schema is None:
            raise ParseError("Schema is none", "convertRam2Xml")
        node = self.create_schema(schema)
        domains = self.xml.createElement("domains")
        for domain in self.create_domain(schema.domains):
            domains.appendChild(domain)
        node.appendChild(domains)

        tables = self.xml.createElement("tables")
        for table in self.create_table(schema.tables):
            tables.appendChild(table)
        node.appendChild(tables)

        self.xml.appendChild(node)
        return self.xml

    def _create_constraint_detail_dom(self, detail):
        detail_dom = self.xml.createElement('item')
        if detail.value:
            detail_dom.setAttribute('value', detail.value)
        return detail_dom

    def _create_index_detail_dom(self, detail):
        detail_dom = self.xml.createElement('item')
        if detail.value:
            detail_dom.setAttribute('value', detail.value)
        if detail.expression:
            detail_dom.setAttribute('expression', detail.expression)
        if detail.descend:
            detail_dom.setAttribute('descend', detail.descend)
        return detail_dom