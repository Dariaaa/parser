from db.sqlite_ddl_init import SQL_DBD_Init

import uuid
import os
import errno
import sqlite3
import configparser

class DBUploader:

    def __init__(self, config_file, db_file_name):

        self.config = configparser.ConfigParser()
        self.config.read(config_file, 'utf-8')

        self._drop_if_exists(db_file_name)
        self.conn = sqlite3.connect(db_file_name)
        self.cursor = self.conn.cursor()

    def __exit__(self):
        self.conn.close()

    def init_dbd(self):
        """
        Create empty sqlite database
        :return:
        """
        self.cursor.executescript(SQL_DBD_Init)

    def create_tmb_dbd(self):
        """
        Create temp table which will contain relationship
        of domain table and datatype table
        :return:
        """
        query = self.config.get('CREATE', 'temp_rel_domain_datatype')
        self.cursor.execute(query)

    def add_rel_domains_datatypes(self, schema):
        """
        Fill temp table
        Create row contains domain name and data type name
        :param schema: Schema
        :return:
        """
        query = self.config.get('INSERT', 'add_rel_to_temp')
        for domain in schema.domains:
            self.cursor.execute(query, {
                "domain_name" : domain.name,
                "datatype_name": domain.type
            })

    def add_schema(self, schema):
        """
        Create new schema in database
        :param schema:
        :return:
        """
        query = self.config.get('INSERT', 'schema')

        self.cursor.execute(query, {
            "name": schema.name,
        })


    def get_result(self):
        """
        Get result executing query
        :return:
        """
        columns = [column[0] for column in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results


    def update_rel_domains_datatypes(self):
        """
        Update relationship between domain table and data type table
        :return:
        """
        query = self.config.get('UPDATE', 'domain_datatype_rel')
        self.cursor.execute(query)

    def drop_tmp(self):
        """
        Delete temp table
        :return:
        """
        query = self.config.get('DROP', 'temp')
        self.cursor.execute(query)

    @staticmethod
    def _drop_if_exists(file_name: str):
        """
        Delete data base file if it exists
        :param file_name:
        :return:
        """
        try:
            os.remove(file_name)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    def get_schema_id(self, schema):
        query = self.config.get("SELECT", "get_schema_id")
        self.cursor.execute(query, {
            "name": schema.name
        })
        result = self.get_result()

        schema_id = result[0]["id"]
        return schema_id

    def get_id(self,table):
        """
        Get all ids
        :param self:
        :return:
        """
        query = self.config.get("SELECT", "get_"+table+"_id")
        self.cursor.execute(query)
        result_map = {}
        for result_obj in self.get_result():
            result_map[result_obj["name"]] = result_obj["id"]
        return result_map

    def add_domains(self, schema):
        """
        Add domains to database from Schema
        :param schema: Schema
        :return:
        """
        query = self.config.get('INSERT', 'domain')
        for domain in schema.domains:
            self.cursor.execute(query, {
                'name': domain.name,
                'description': domain.descr,
                'length': domain.length,
                'char_length': domain.char_length,
                'precision': domain.precision,
                'scale': domain.scale,
                'width': domain.width,
                'align': domain.align,
                'show_null': domain.show_null,
                'show_lead_nulls': domain.show_lead_nulls,
                'thousands_separator': domain.thousands_separator,
                'summable': domain.summable,
                'case_sensitive': domain.case_sensitive,
                'data_type_id': 1,
                'uuid': uuid.uuid1().hex
            })

    def add_table(self, table, schema_id):
        """
        Add table to database from Table
        :param table:
        :param schema:
        :param schema_id:
        :return:
        """
        query = self.config.get('INSERT', 'table')
        self.cursor.execute(query, {
            'schema_id': schema_id,
            'name': table.name,
            'description': table.descr,
            'can_add': table.add,
            'can_edit': table.edit,
            'can_delete': table.delete,
            'temporal_mode': table.temporal_mode,
            'means': table.means,
            'uuid': uuid.uuid1().hex
        })
        table_id = self.cursor.lastrowid
        return table_id

    def add_field(self, table_id, field, field_position, domain_id):
        """
        Add fields to database from Table
        :param table_id:
        :param field:
        :param field_position:
        :param domain_id:
        :return:
        """

        query = self.config.get('INSERT', 'field')
        self.cursor.execute(query, {
            'table_id': table_id,
            'position': field_position,
            'name': field.name,
            'russian_short_name': field.rname,
            'description': field.descr,
            'domain_id': domain_id,
            'can_input': field.input,
            'can_edit': field.edit,
            'show_in_grid': field.show_in_grid,
            'show_in_details': field.show_in_details,
            'is_mean': field.is_mean,
            'autocalculated': field.autocalculated,
            'required': field.required,
            'uuid': uuid.uuid1().hex

        })

    def add_constraint(self, table_id, constraint):
        query = self.config.get('INSERT', 'constraint')
        self.cursor.execute(query, {
            'table_id': table_id,
            'name': constraint.name,
            'constraint_type': constraint.kind,
            'unique_key_id': 1,
            'reference': constraint.reference,
            'has_value_edit': constraint.has_value_edit,
            'cascading_delete': constraint.cascading_delete,
            'expression': constraint.expression,
            'uuid': uuid.uuid1().hex
        })


    def add_constraint_detail(self, detail, constraint, field_id):

        query = self.config.get('INSERT', 'constraint_detail')
        self.cursor.execute(query, {
            'constraint_id': id(constraint),
            'position': constraint.details.index(detail),
            'field_id': field_id
        })

    def add_index(self, table_id,  index):

        query = self.config.get('INSERT', 'index')
        self.cursor.execute(query, {
            'id': id(index),
            'table_id': table_id,
            'name': index.name,
            'local': index.local,
            'kind': index.kind,
            'uuid': uuid.uuid1().hex
        })

    def add_index_detail(self, detail, index, field_id):

        query = self.config.get('INSERT', 'index_detail')
        self.cursor.execute(query, {
            'index_id': id(index),
            'position': index.details.index(detail),
            'field_id': field_id,
            'expression': detail.expression,
            'descend': detail.descend
        })

    def upload(self, schema):
        """
        Upload Schema to sqlite database
        :param schema: Schema
        :return:
        """
        self.init_dbd()
        self.add_schema(schema)
        schema_id = self.get_schema_id(schema)

        self.add_domains(schema)

        domains_ids = self.get_id("domains")


        for table in schema.tables:
            table_id = self.add_table(table, schema_id)
            for field in table.fields:
                field_position = list(table.fields).index(field)
                domain_id = domains_ids[field.domain]
                self.add_field(table_id, field, field_position, domain_id)
            fields_ids = self.get_id("fields")
            for constraint in table.constraints:
                self.add_constraint(table_id, constraint)
                for detail in constraint.details:
                    field_id = fields_ids[detail.value]
                    self.add_constraint_detail(detail,constraint, field_id)
            for index in table.indexes:
                self.add_index(table_id, index)
                for detail in index.details:
                    field_id = fields_ids[detail.value]
                    self.add_index_detail(detail,index, field_id)

        #   updating unique key for constraints
        query = self.config.get('UPDATE', 'update_unique_key')
        self.cursor.execute(query)



        self.create_tmb_dbd()
        self.add_rel_domains_datatypes(schema)
        self.update_rel_domains_datatypes()
        self.drop_tmp()
        self.conn.commit()
