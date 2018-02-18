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
        scripts.append('\n'.join([
            self.create_domain_ddl(d, schema)
            for d in schema.domains
        ]))

        foreign = []

        for table in schema.tables:
            scripts.append(self.create_table_ddl(table, schema))

            for index in table.indexes:
                scripts.append(self.create_index_ddl(index, table, schema))

            for constraint in table.constraints:
                if constraint.kind.lower() == 'foreign':
                    foreign.append(self.create_constraint_ddl(constraint, table, schema))
                else:
                    scripts.append(self.create_constraint_ddl(constraint, table, schema))

        scripts.append('\n'.join(foreign))
        scripts.append('COMMIT;')

        queries = '\n'.join(scripts)

        return queries


    def create_schema_ddl(self,schema: Schema):
        return "CREATE SCHEMA {};".format(schema.name)

    def create_domain_ddl(self, domain:Domain, schema:Schema):
        try:
            ddl =  """CREATE DOMAIN {}."{}" AS {}; """\
                .format(schema.name, domain.name, get_type_in_postgres(domain))
        except TypeNotFoundException:
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
        return """\"{}\" {}.\"{}\""""\
            .format(field.name,schema.name,field.domain)


    def get_fields_ddl_part(self,table:Table,schema:Schema):
        return ",".join([self.create_field_ddl(field,schema)
                           for field in table.fields])

    def create_constraint_ddl(self,constraint:Constraint,table:Table,schema:Schema):
        details = []
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


    def create_index_ddl(self,index: Index, table: Table, schema: Schema):
        details = []
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



