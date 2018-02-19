# parser
repository contains implementations tasks on the subject "collective development" by Daria Karpenko.

## structure

```
src
  │   mssql2pg.py - loading metadata from mssql db and creating ddl instructions 
  │                 and uploading this metadata to sqlite db;
  │                 transfering data from mssql db to postgres sql db 
  │                  
  │   init_pgdb.py - loading metadata from db or xdb file and uploading to postgresql db
  │   dbd2xml.py - loading from sqlite db and write to xml file
  │   xml2dbd.py - parsing from xml file and uploading to sqite db
  │ 
  ├───data_transfering
  │       data_transfering.py   - transfering data from mssql db to postgresql db 
  │ 
  ├───db
  │       config.py             - contains url's and path's which uses in program
  │       mssql_queries.py      - contains sql queries for mssql database
  │       postgres_util.py      - util for postgresql
  │       sqlite_ddl_init.py    - queries for creating sqlite database
  │       sqlite_queries.py     - contains sql queries for sqilte database
  │
  ├───dbd_module
  │       dbd2ram.py            - loading from database
  │
  ├───ram_module
  │       ram2dbd.py            - uploading to database
  │       ram2dbd_postgres.py   - contains sql queries for postgresql database
  │       ram2xml.py            - converting from ram representation to xml file
  │       ram_structure.py      - ram classes
  ├───test
  │       test.py               - contains checking result of parsing and downloading data
  │
  ├───utils
  │       exceptions.py         - contains custom exceptions which uses in some modules
  │       minidom_fixed.py      - util for xml
  │       writer.py             - writing files
  │
  └────xml_module
          xml2ram.py            - creating ram representation of xml file
```
modules that were implemented:
1. a мodule of converting from text representation of database to representation in RAM (`xml2ram`)
2. a мodule of converting from object representation of database to text representation (`ram2xml`)
3. a мodule of uploading a RAM representation to the SQLite database (`ram2dbd`)
4. a module of loading the DBD representation and converting it into a RAM representation (`dbd2ram`)
5. a module of uploading from RAM representation of database to PostgreSQL database (`ram2dbd_postgres`)