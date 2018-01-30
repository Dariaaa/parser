from db.sqlite_ddl_init import SQL_DBD_Init
from db.sql.sql_const import add_schema_sql
from db.sql.sql_const import add_domains_sql
from db.sql.sql_const import add_temp_table_sql
from db.sql.sql_const import fill_temp_table_sql
from db.sql.sql_const import drop_temp_table_sql
from db.sql.sql_const import update_rel_domain_datatype
from itertools import count

import os
import errno
import sqlite3


class DBUploader:

    def __init__(self, db_file_name):
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
        self.cursor.execute(add_temp_table_sql)

    def add_rel_domains_datatypes(self, schema):
        """
        Fill temp table
        Create row contains domain name and data type name
        :param schema: Schema
        :return:
        """
        self.cursor.executemany(fill_temp_table_sql, [(d.name, d.type) for d in schema.domains])

    def add_schema(self, schema):
        """
        Create new schema in database
        :param schema:
        :return:
        """
        self.cursor.execute(add_schema_sql.format(schema.name))

    def add_domains(self, schema):
        """
        Add domains to database from Schema
        :param schema: Schema
        :return:
        """
        it = count()
        self.cursor.executemany(add_domains_sql, [(
                   d.name,
                   d.descr,
                   d.length,
                   d.char_length,
                   d.precision,
                   d.scale,
                   d.width,
                   d.align,
                   d.show_null,
                   d.show_lead_nulls,
                   d.thousands_separator,
                   d.summable,
                   d.case_sensitive,
                   1,
                   next(it)
               ) for d in schema.domains]
           )

    def update_rel_domains_datatypes(self):
        """
        Update relationship between domain table and data type table
        :return:
        """
        self.cursor.execute(update_rel_domain_datatype)

    def drop_tmp(self):
        """
        Delete temp table
        :return:
        """
        self.cursor.execute(drop_temp_table_sql)

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

    def upload(self, schema):
        """
        Upload Schema to sqlite database
        :param schema: Schema
        :return:
        """
        self.init_dbd()
        self.add_schema(schema)
        self.add_domains(schema)
        self.create_tmb_dbd()
        self.add_rel_domains_datatypes(schema)
        self.update_rel_domains_datatypes()
        self.drop_tmp()
        self.conn.commit()
