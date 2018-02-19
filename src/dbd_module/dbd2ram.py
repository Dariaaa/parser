import sqlite3
import pyodbc

from ram_module.ram_structure import Schema, IndexDetail, ConstraintDetail, Index, Constraint, Field, Table, Domain
from utils.exceptions import ParseError


class DBDownloader:
    """
    Downloading data to xml from sqlite database
    Data represents as map<column_name,value>
    """
    def __init__(self, queries, db_path, db_url):
        self.config = queries

        if db_path:
            self.conn = sqlite3.connect(db_path)
        if db_url:
            self.conn = pyodbc.connect(db_url)

        self.cursor = self.conn.cursor()

    def __exit__(self):
        self.conn.close()

    def _get_result(self):
        """
        Get last result executing query
        :return:
        """
        columns = [column[0] for column in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def load_schema(self):
        """
        Download schema as map
        :return:
        """
        query = self.config.get_schemas
        self.cursor.execute(query)
        return self._get_result()

    def load_domains(self):
        query = self.config.get_domains
        self.cursor.execute(query)
        return self._get_result()

    def load_tables(self):
        query = self.config.get_tables
        self.cursor.execute(query)
        return self._get_result()

    def load_fields(self):
        query = self.config.get_fields
        self.cursor.execute(query)
        return self._get_result()

    def load_constraints(self):
        query = self.config.get_constraints
        self.cursor.execute(query)
        return self._get_result()

    def load_index(self):
        query = self.config.get_indices
        self.cursor.execute(query)
        return self._get_result()

    def load_constraint_details(self):
        query = self.config.get_constraint_details
        self.cursor.execute(query)
        return self._get_result()

    def load_index_details(self):
        query = self.config.get_index_details
        self.cursor.execute(query)
        return self._get_result()


    def load(self):
        schemas = {}
        for row in self.load_schema():
            schema, schema_id = self.create_schema(row)
            schemas[schema_id] = schema
        tables = {}
        for row in self.load_tables():
            table, table_id, schema_id = self.create_table(row)
            tables[table_id] = table
            schemas[schema_id].tables.append(table)

        domains = {}
        l_d = self.load_domains()
        for row in l_d:
            domain, domain_id = self.create_domain(row)
            domains[domain_id] = domain
        for schema in [schema for schema in schemas.values() if len(schema.tables) > 0]:
            schema.domains = domains

        fields = {}
        for row in self.load_fields():
            field, field_id, table_id = self.create_field(row)
            if table_id not in tables:
                continue
            tables[table_id].fields.append(field)
            fields[field_id] = field

        constraints = {}
        for row in self.load_constraints():
            constraint, constraint_id, table_id = self.create_constraint(row)
            if table_id not in tables:
                continue
            tables[table_id].constraints.append(constraint)
            constraints[constraint_id] = constraint
            if constraint.reference in tables.keys():
                constraint.reference = tables[constraint.reference].name;


        indices = {}
        for row in self.load_index():
            index, index_id, table_id = self.create_index(row)
            if table_id not in tables:
                continue
            tables[table_id].indexes.append(index)
            indices[index_id] = index

        constraint_details = {}
        for row in self.load_constraint_details():
            detail, detail_id, constraint_id = self.create_constraint_detail(row)
            constraints[constraint_id].details.append(detail)
            constraint_details[detail_id] = detail

        index_details = {}
        for row in self.load_index_details():
            detail, detail_id, index_id = self.create_index_detail(row)
            if index_id not in indices:
                continue
            indices[index_id].details.append(detail)
            index_details[detail_id] = detail
        return schemas



    def create_schema(self, schema_row):
        schema = Schema()
        schema_id = None
        for attr in schema_row:
            if attr == 'name':
                schema.name = schema_row[attr]
            elif attr == 'fulltext_engine':
                schema.fulltext_engine = schema_row[attr]
            elif attr == 'version':
                schema.version = schema_row[attr]
            elif attr == 'description':
                schema.descr = schema_row[attr]
            elif attr == 'id':
                schema_id = schema_row[attr]
            else:
                raise ParseError("Unsupported attribute {}".format(attr), self)
        return schema, schema_id

    def create_domain(self,attr_dict):
        domain = Domain()

        domain_id = None
        for attr in attr_dict:
            if attr == 'name':
                domain.name = attr_dict[attr]
            elif attr == 'data_type_name':
                domain.type = attr_dict[attr]
            elif attr == 'data_type_id':
                domain.type = attr_dict[attr]
            elif attr == 'align':
                domain.align = attr_dict[attr]
            elif attr == 'width':
                domain.width = attr_dict[attr]
            elif attr == 'char_length':
                domain.char_length = attr_dict[attr]
            elif attr == 'description':
                domain.descr = attr_dict[attr]
            elif attr == 'length':
                domain.length = attr_dict[attr]
            elif attr == 'scale':
                domain.scale = attr_dict[attr]
            elif attr == 'precision':
                domain.precision = attr_dict[attr]
            elif attr == 'case_sensitive':
                domain.case_sensitive = attr_dict[attr]
            elif attr == 'show_null':
                domain.show_null = attr_dict[attr]
            elif attr == 'show_lead_nulls':
                domain.show_lead_nulls = attr_dict[attr]
            elif attr == 'thousands_separator':
                domain.thousands_separator = attr_dict[attr]
            elif attr == 'summable':
                domain.summable = attr_dict[attr]
            elif attr == 'id':
                domain_id = attr_dict[attr]
            else:
                raise ParseError("Unsupported attribute {}".format(attr),self)
        return domain, domain_id

    def create_table(self,attr_dict):
        table = Table()

        table_id = None
        schema_id = None

        for attr in attr_dict:
            if attr == 'name':
                table.name = attr_dict[attr]
            elif attr == 'description':
                table.descr = attr_dict[attr]
            elif attr == 'temporal_mode':
                table.ht_table_flags = attr_dict[attr]
            elif attr == 'access_level':
                table.access_level = attr_dict[attr]
            elif attr == 'can_add':
                table.add = attr_dict[attr]
            elif attr == 'can_edit':
                table.edit = attr_dict[attr]
            elif attr == 'can_delete':
                table.delete = attr_dict[attr]
            elif attr == 'means':
                table.means = attr_dict[attr]
            elif attr == 'schema_id':
                schema_id = attr_dict[attr]
            elif attr == 'id':
                table_id = attr_dict[attr]
            else:
                raise ParseError("Unsupported attribute {}".format(attr),self)
        return table, table_id, schema_id

    def create_field(self,attr_dict):
        field = Field()

        field_id = None
        table_id = None

        for attr in attr_dict:
            if attr == 'name':
                field.name = attr_dict[attr]
            elif attr == 'russian_short_name':
                field.rname = attr_dict[attr]
            elif attr == 'domain_name':
                field.domain = attr_dict[attr]
            elif attr == 'type':
                field.type = attr_dict[attr]
            elif attr == 'description':
                field.descr = attr_dict[attr]
            elif attr == 'can_input':
                field.input = attr_dict[attr]
            elif attr == 'can_edit':
                field.edit = attr_dict[attr]
            elif attr == 'show_in_grid':
                field.show_in_grid = attr_dict[attr]
            elif attr == 'show_in_details':
                field.show_in_details = attr_dict[attr]
            elif attr == 'is_mean':
                field.is_mean = attr_dict[attr]
            elif attr == 'autocalculated':
                field.autocalculated = attr_dict[attr]
            elif attr == 'required':
                field.required = attr_dict[attr]
            elif attr == 'id':
                field_id = attr_dict[attr]
            elif attr == 'table_id':
                table_id = attr_dict[attr]
            else:
                raise ParseError("Unsupported attribute {}".format(attr),self)
        return field, field_id, table_id

    def create_constraint(self,attr_dict):
        constraint = Constraint()

        if attr_dict is None:
            return constraint

        constraint_id = None
        table_id = None

        for attr in attr_dict:
            if attr == 'name':
                constraint.name = attr_dict[attr]
            elif attr == 'constraint_type':
                constraint.kind = attr_dict[attr]
            elif attr == 'items':
                detail = ConstraintDetail()
                detail.value = attr_dict[attr]
                constraint.details.append(detail)
            elif attr == 'reference':
                constraint.reference = attr_dict[attr]
            elif attr == 'unique_key_id':
                constraint.constraint = attr_dict[attr]
            elif attr == 'expression':
                constraint.expression = attr_dict[attr]
            elif attr == 'has_value_edit':
                constraint.has_value_edit = attr_dict[attr]
            elif attr == 'cascading_delete':
                constraint.cascading_delete = attr_dict[attr]
            elif attr == 'id':
                constraint_id = attr_dict[attr]
            elif attr == 'table_id':
                table_id = attr_dict[attr]
            else:
                raise ParseError("Unsupported attribute {}".format(attr),self)
        return constraint, constraint_id, table_id

    def create_index(self,attr_dict):
        index = Index()

        if attr_dict is None:
            return index

        index_id = None
        table_id = None

        for attr in attr_dict:
            if attr == 'name':
                index.name = attr_dict[attr]
            elif attr == 'field':
                detail = IndexDetail()
                detail.value = attr_dict[attr]
                index.details.append(detail)
            elif attr == 'kind':
                index.kind = attr_dict[attr]
            elif attr == 'local':
                index.local = attr_dict[attr]
            elif attr == 'uniqueness':
                index.uniqueness = attr_dict[attr]
            elif attr == 'fulltext':
                index.fulltext = attr_dict[attr]
            elif attr == 'id':
                index_id = attr_dict[attr]
            elif attr == 'table_id':
                table_id = attr_dict[attr]
            else:
                raise ParseError("Unsupported attribute {}".format(attr),self)
        return index, index_id, table_id

    def create_constraint_detail(self,attr_dict):
        detail = ConstraintDetail()

        detail_id = None
        constraint_id = None

        for attr in attr_dict:
            if attr == 'field_name':
                detail.value = attr_dict[attr]
            elif attr == 'id':
                detail_id = attr_dict[attr]
            elif attr == 'constraint_id':
                constraint_id = attr_dict[attr]
            else:
                raise ParseError("Unsupported attribute {}".format(attr),self)
        return detail, detail_id, constraint_id

    def create_index_detail(self,attr_dict):
        detail = IndexDetail()

        detail_id = None
        index_id = None

        for attr in attr_dict:
            if attr == 'field_name':
                detail.value = attr_dict[attr]
            elif attr == 'expression':
                detail.expression = attr_dict[attr]
            elif attr == 'descend':
                detail.descend = attr_dict[attr]
            elif attr == 'id':
                detail_id = attr_dict[attr]
            elif attr == 'index_id':
                index_id = attr_dict[attr]
            else:
                raise ParseError("Unsupported attribute {}".format(attr),self)
        return detail, detail_id, index_id

