import postgresql
import pyodbc
from ram_module.ram2dbd_postgres import DBInitialisator


class DataTransfering:
    def __init__(self, db_name, mssql_url,pg_url):
        self.db_name = db_name
        self.pg_server = pg_url
        self.mssql_server = mssql_url
        self.mssql_con = pyodbc.connect(self.mssql_server)
        self.pg_con = postgresql.open(self.pg_server)
        self.cursor = self.mssql_con.cursor()


    def __exit__(self):
        self.mssql_con.close()
        self.pg_con.close()

    def create_empty_db(self):
        pg_init = DBInitialisator()
        ddl = pg_init.drop_database(self.db_name)
        self.pg_con.execute(ddl)
        ddl = pg_init.create_database_ddl(self.db_name)
        self.pg_con.execute(ddl)
        self.pg_con.close()
        self.pg_con = postgresql.open(self.pg_server +"/"+ self.db_name.lower())

    def start(self,schemas):
        self.pg_con.execute('BEGIN TRANSACTION;')
        self.pg_con.execute('SET CONSTRAINTS ALL DEFERRED;')
        for schema in schemas.values():
            for table in schema.tables:
                self.cursor.execute('BEGIN TRANSACTION;')
                self.cursor.execute(self.select_query(schema,table))
                rows = self.cursor.fetchall()
                query = ''
                for row in rows:

                    s ="alter table {}.\"{}\" disable trigger all;".format(schema.name,table.name)
                    s += self.insert_query(schema, table, row) + ";\n"
                    s+="alter table {}.\"{}\" enable trigger all;".format(schema.name,table.name)
                    print(s)
                    query+= s

                    self.pg_con.execute(s)
                self.cursor.execute('COMMIT;')

        self.pg_con.execute('COMMIT TRANSACTION;')

    def select_query(self,schema,table):
        fields = []
        for field in table.fields:
            _str = '[{}]'.format(field.name)
            fields.append(_str)
        ss = ','.join(fields)
        query = 'SELECT {0} FROM [{1}].[{2}]'.format(ss,schema.name,table.name)
        print(query)
        return query

    def insert_query(self,schema, table, values):
        fields = []
        for field in table.fields:
            fields.append('{}'.format(field.name))
        _values = []
        for value in values:
            val = str(value).replace('\'','') if value is not None else 'NULL'
            if val=='NULL':
                _values.append(val)
            else:
                _values.append('\'{}\''.format(val))
        query = 'INSERT INTO {}."{}" ({}) VALUES ({})'.format(schema.name, table.name,', '.join(fields),', '.join(_values))

        return query