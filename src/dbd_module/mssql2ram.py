import pyodbc

from db.postgres_util import get_type_in_postgres
from ram_module.ram_structure import Schema, Table, Index, Constraint, Field, Domain


class MSSQLDownloader:
    def __init__(self,queries,url):
        self.queries = queries
        self.url = url
        self.conn = pyodbc.connect(url)
        self.cursor = self.conn.cursor()

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

    def load_schema(self, schema_name:str):
        schema = Schema()
        schema.name = schema_name
        schema.tables = self.load_table(schema)

        return schema

    def load_table(self, schema:Schema):
        self.cursor.execute(self.queries.get_tables,schema.name)
        rows = self._get_result()
        list = []
        for row in rows:
            table = Table()
            # print(table)
            table.name = row['name']
            table.add = bool(row['addition'])
            table.edit = bool(row['edition'])
            table.temporal_mode = bool(row['temporal_type'])
            table.indexes = self.load_indices(schema.name, table.name)
            table.constraints = self.load_constraints(schema.name, table.name)
            table.fields = self.load_fields(table.name)

            list.append(table)
        return list

    def load(self,schema_name):
        return self.load_schema(schema_name)

    def load_indices(self, schema_name:str, table_name:str):
        self.cursor.execute(self.queries.get_indices, "{0}.{1}".format(schema_name,table_name))
        rows = self._get_result()
        list = []
        for row in rows:
            index = Index()
            # print(row)
            index.name = row['index_name']
            if bool(row['is_unique']) :
                index.kind = 'uniqueness'
            elif bool(row['is_fulltext']):
                index.kind = 'fulltext'
            else : index.kind = ''
            index.items = row['field_name']
            list.append(index)
        return list

    def load_constraints(self, schema_name:str, table_name:str):
        self.cursor.execute(self.queries.get_primary_keys, "{0}.{1}".format(schema_name, table_name))
        rows = self._get_result()
        primary = []
        for row in rows:
            # print(row)
            constraint = Constraint()
            constraint.name = row['name']
            constraint.items = row['items']
            constraint.kind = "PRIMARY"
            constraint.unique_key_id  = row['unique_key_index']
            primary.append(constraint)


        self.cursor.execute(self.queries.get_foreign_keys, "{0}.{1}".format(schema_name, table_name))
        rows = self._get_result()
        foreign = []
        for row in rows:
            # print(row)
            constraint = Constraint()
            constraint.name = row['name']
            constraint.kind = "FOREIGN"
            constraint.items = row['items']
            constraint.reference = row['reference']
            constraint.cascading_delete = bool(row['cascading_delete'])
            foreign.append(constraint)

        return primary + foreign

    def load_fields(self, table_name:str):
        self.cursor.execute(self.queries.get_fields, table_name)
        rows = self._get_result()
        list = []
        for row in rows:
            # print(row)
            field = Field()
            field.name = row['name']
            field.domain = row['dom']
            field.position = str(row['position'])
            field.edit = row['edit']
            field.show_in_grid = row['show_in_grid']
            field.autocalculated = row['autocalculated']
            field.required = row['required']
            field.input = not (field.autocalculated or field.edit)
            domain = Domain()
            domain.char_length = str(row['max_length'])
            domain.precision = str(row['precision'])
            domain.scale = str(row['scale'])
            domain.type = row['DATA_TYPE']
            domain.type = get_type_in_postgres(domain)
            field.domain = domain
            list.append(field)
        return list
