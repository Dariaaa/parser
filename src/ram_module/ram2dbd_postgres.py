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

    def generate_ddl(self, schema: Schema, mssql):
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

            for index in table.indexes:
                scripts.append(self.create_index_ddl(index, table, schema))

            if mssql:
                pr = self.create_primary(table,schema)
                fr = self.create_foreign(table,schema)
                if pr !='':
                    primary.append(pr)
                if fr !='':
                    foreign.append(fr)
            else:
                for constraint in table.constraints:
                    if constraint.kind.lower() == 'foreign':
                        foreign.append(self.create_constraint_ddl(constraint, table, schema))
                    else:
                        scripts.append(self.create_constraint_ddl(constraint, table, schema))

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

    def create_constraint_ddl(self,constraint:Constraint,table:Table,schema:Schema):
        details = []
        if constraint.details:
            for det in constraint.details:
                detail = r'"' + det.value + r'"'
                details.append(detail)

            if constraint.kind.lower() == 'primary':
                str = """PRIMARY KEY ({})"""\
                    .format(', '.join(details))
            elif constraint.kind.lower() == 'foreign':
                str = """FOREIGN KEY ({}) REFERENCES {}."{}" DEFERRABLE"""\
                    .format(', '.join(details),schema.name,
                        constraint.reference,constraint.name)
            else: return ''

            return """ALTER TABLE {}."{}" ADD {};"""\
                .format(schema.name,table.name,str)
        else:
            query = """alter table {}."{}"\n add {} ({})\n"""\
                .format(schema.name,table.name,constraint.kind + " KEY", constraint.items)

            if constraint.kind.lower() == 'foreign':
                query+="""references {}.\"{}\" """.format(schema.name,constraint.reference)
            query +=";"
            return query


    def create_index_ddl(self,index: Index, table: Table, schema: Schema):
        details = []
        if index.details:
            for det in index.details:
                detail = '\"' + det.value + '\"'
                if det.expression:
                    detail += ' (' + det.expression + ')'
                if not det.descend:
                    detail += ' ASC'
                else:
                    detail += det.descend.upper()
                details.append(detail)

            if len(details) == 0:
                return ''

            return """CREATE INDEX {} ON {}."{}"({});"""\
                .format('"' + index.name + table.name + '"' if index.name else '',
                        schema.name,table.name,', '.join(details))
        else:
            unique = "UNIQUE " if index.kind =="uniqueness" else ""

            return """CREATE {0} INDEX  ON {1}."{2}" ({3});""".format(
                unique ,schema.name,table.name,index.items)



