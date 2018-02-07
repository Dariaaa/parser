import postgresql
from ram_module import Schema,Domain,Table,Field,\
    Constraint,Index
from .postgres_util import get_type_in_postgres

class DBInitialisator:
    """

        Connect and create empty postgresql database

    """
    def __init__(self):
        self.url = 'pq://postgres:123@localhost:5432'
        self.conn = postgresql.open(self.url)


    def __exit__(self):
        self.conn.close()

    def create_database(self, db_name):
        self.conn.execute('DROP DATABASE IF EXISTS ' + db_name)
        self.conn.execute('CREATE DATABASE ' + db_name)
        self.conn.close()
        self.conn = postgresql.open(self.url + '/' + db_name.lower())


    def create_schema_ddl(self,schema: Schema):
        return "CREATE SCHEMA {};".format(schema.name)


    def create_domain_ddl(self, domain:Domain, schema:Schema):
        ddl =  """CREATE DOMAIN {}."{}" AS {}; """\
            .format(schema.name, domain.name, get_type_in_postgres(domain))
        if (domain.descr):
            ddl+= """COMMENT ON DOMAIN {}."{}" IS \'{}\';"""\
            .format(schema.name,domain.name,domain.descr)
        return ddl

    def create_table_ddl(self,table:Table,schema:Schema):
        return """CREATE TABLE {}."{}" ({});"""\
            .format(schema.name,table.name,
            self.get_fields_ddl_part(table,schema))

    def create_field_ddl(self,field:Field,schema:Schema):
        return """\"{}\" {}.\"{}\""""\
            .format(field.name,schema.name,field.domain)


    def get_fields_ddl_part(self,table:Table,schema:Schema):
        return ",".join([self.create_field_ddl(field,schema)
                           for field in table.fields])

    def start(self, database_name:str, schema:Schema):
        self.create_database(database_name)
        scripts = []
        scripts.append('BEGIN TRANSACTION;')
        scripts.append(self.create_schema_ddl(schema))
        scripts.append('\n'.join([
            self.create_domain_ddl(d,schema)
            for d in schema.domains
        ]))
        scripts.append('\n'.join([
            self.create_table_ddl(t, schema)
            for t in schema.tables
        ]))

        scripts.append('COMMIT;')


        queries = '\n'.join(scripts)
        print(queries)
        self.conn.execute(queries)


