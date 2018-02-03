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

    def get_result(self):
        columns = [column[0] for column in self.cursor.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def add_tables(self, schema, schema_id):
        """
        Add domains to database from Schema
        :param schema: Schema
        :param schema_id: Shema id
        :return:
        """
        query = self.config.get('INSERT', 'table')

        for table in schema.tables:
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
        self.add_tables(schema, schema_id)
        self.create_tmb_dbd()
        self.add_rel_domains_datatypes(schema)
        self.update_rel_domains_datatypes()
        self.drop_tmp()
        self.conn.commit()
