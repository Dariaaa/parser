import postgresql

from db.config import postgressql_url, result_path
from ram_module.ram_structure import Schema,Domain,Table,Field,\
    Constraint,Index
from db.postgres_util import get_type_in_postgres
from utils.exceptions import TypeNotFoundException

class DBInitialisator:
    """

        Generate ddl instructions to create postgresql database

    """

    def generate_ddl(self, schema: Schema):
        scripts = []

        scripts.append('BEGIN TRANSACTION;')
        scripts.append(self.create_schema_ddl(schema))
        if schema.domains:
            for d in schema.domains.values():
                ddl = self.create_domain_ddl(d, schema)
                scripts.append(ddl)

        primary = []
        foreign = []

        for table in schema.tables:
            scripts.append(self.create_table_ddl(table, schema))

            scripts.append(self.create_index_ddl(table, schema))


            pr = self.create_primary(table,schema)
            fr = self.create_foreign(table,schema)
            if pr !='':
                primary.append(pr)
            if fr !='':
                foreign.append(fr)

        scripts.append("\n".join(primary))
        scripts.append('\n'.join(foreign))
        scripts.append('COMMIT;')

        # queries = '\n'.join(scripts)

        return scripts

    def drop_database(self,db_name):
        return """DROP DATABASE IF EXISTS {};\n""".format(db_name)

    def create_database_ddl(self,db_name):
        return """CREATE DATABASE {};""".format(db_name)

    def create_schema_ddl(self,schema: Schema):
        return "CREATE SCHEMA {};".format(schema.name)

    def create_domain_ddl(self, domain:Domain, schema:Schema):
        try:
            ddl =  """CREATE DOMAIN {}."{}" AS {}; """\
                .format(schema.name, domain.name, get_type_in_postgres(domain))
        except TypeNotFoundException:
            print(domain.name + " " + domain.type)
            return ''

        if domain.descr:
            ddl+= """COMMENT ON DOMAIN {}."{}" IS \'{}\';"""\
            .format(schema.name,domain.name,domain.descr)
        return ddl

    def create_table_ddl(self,table:Table,schema:Schema):
        return """CREATE TABLE {}."{}" ({});"""\
            .format(schema.name,table.name,
            self.get_fields_ddl_part(table,schema))

    def create_field_ddl(self,field:Field,schema:Schema):
        domain = ''
        if type(field.domain) is Domain:
            domain = field.domain.type
            return """\n{} {}""".format(field.name, domain)
        else:
            domain = field.domain
        return """\"{}\" {}.\"{}\""""\
            .format(field.name,schema.name,domain)


    def get_fields_ddl_part(self,table:Table,schema:Schema):
        return ",".join([self.create_field_ddl(field,schema)
                           for field in table.fields])


    def create_primary(self,table:Table,schema:Schema):
        prim = []
        for c in table.constraints:
            if c.kind.lower() == 'primary':
                prim.append(c.items)
        return """alter table {}."{}" add {} ({}); """ \
                   .format(schema.name, table.name, "PRIMARY KEY", ','.join(prim))

    def create_foreign(self,table:Table,schema:Schema):
        f = ''
        for c in table.constraints:
            if c.kind.lower()=='foreign':
                f += """alter table {}."{}"  add {} ({}) references {}.\"{}\";\n""" \
                    .format(schema.name, table.name, "FOREIGN KEY", c.items, schema.name, c.reference)
        return f

    def create_index_ddl(self,table: Table, schema: Schema):
        ind = []
        ddl = ""
        for i in table.indexes:
            if i.kind == "uniqueness":
                ind.append(i.items)
            else:
                ddl+="""CREATE INDEX  ON {}."{}" ({});\n""".format(
                schema.name,table.name,i.items)
        return """CREATE UNIQUE INDEX  ON {}."{}" ({});\n""".format(
                schema.name,table.name,','.join(ind)) + ddl



