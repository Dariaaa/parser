
temp_rel_domain_datatype = """
    CREATE TABLE dbd$tmpdatatype
        (domain_name varchar NOT NULL
        ,datatype_name varchar NOT NULL)
"""
temp_rel_constraint_table = """
    CREATE TABLE dbd$tmpconsttable
        (constraint_id integer,
        table_name varchar)
"""
update_rel_constraints_table = """

    UPDATE dbd$constraints SET
        reference = (
        SELECT id FROM dbd$tables as t
        JOIN dbd$tmpconsttable t_t
        ON (t.name = t_t.table_name)
        WHERE dbd$constraints.id = t_t.constraint_id)
"""

drop_rel_constraints_table = "DROP table dbd$tmpconsttable"

tmp_const_table = """
    INSERT INTO dbd$tmpconsttable (
        constraint_id,
        table_name
    )VALUES(
        :constraint_id,
        :table_name
    )
"""
insert_schema ="""
    INSERT INTO dbd$schemas (
         name
        ,fulltext_engine
        ,version
        ,description
    )
    VALUES (
         :name
        ,:fulltext_engine
        ,:version
        ,:description
    )
"""

add_rel_to_temp = """
    INSERT INTO dbd$tmpdatatype
        VALUES(
        :domain_name
        ,:datatype_name)

"""
insert_domain  = """
    INSERT INTO dbd$domains (
        name
        ,description
        ,length
        ,char_length
        ,precision
        ,scale
        ,width
        ,align
        ,show_null
        ,show_lead_nulls
        ,thousands_separator
        ,summable
        ,case_sensitive
        ,data_type_id
        ,uuid
    )
    VALUES (
         :name
        ,:description
        ,:length
        ,:char_length
        ,:precision
        ,:scale
        ,:width
        ,:align
        ,:show_null
        ,:show_lead_nulls
        ,:thousands_separator
        ,:summable
        ,:case_sensitive
        ,:data_type_id
        ,:uuid
    )
"""
insert_table  = """
    INSERT INTO dbd$tables (
         schema_id
        ,name
        ,description
        ,can_add
        ,can_edit
        ,can_delete
        ,temporal_mode
        ,means
        ,uuid
    )
    VALUES (
         :schema_id
        ,:name
        ,:description
        ,:can_add
        ,:can_edit
        ,:can_delete
        ,:temporal_mode
        ,:means
        ,:uuid
    )
"""
insert_field = """
     INSERT INTO dbd$fields (
             table_id
            ,position
            ,name
            ,russian_short_name
            ,description
            ,domain_id
            ,can_input
            ,can_edit
            ,show_in_grid
            ,show_in_details
            ,is_mean
            ,autocalculated
            ,required
            ,uuid
        )
     VALUES (
         :table_id
        ,:position
        ,:name
        ,:russian_short_name
        ,:description
        ,:domain_id
        ,:can_input
        ,:can_edit
        ,:show_in_grid
        ,:show_in_details
        ,:is_mean
        ,:autocalculated
        ,:required
        ,:uuid
     )
"""
insert_constraint ="""
     INSERT INTO dbd$constraints (
             table_id
            ,name
            ,constraint_type
            ,reference
            ,unique_key_id
            ,has_value_edit
            ,cascading_delete
            ,expression
            ,uuid
        )
     VALUES (
             :table_id
            ,:name
            ,:constraint_type
            ,:reference
            ,:unique_key_id
            ,:has_value_edit
            ,:cascading_delete
            ,:expression
            ,:uuid
     )
"""
insert_constraint_detail = """
    INSERT INTO dbd$constraint_details (
         constraint_id
        ,position
        ,field_id
    )
    VALUES (
         :constraint_id
        ,:position
        ,:field_id
    )
"""
insert_index ="""
    INSERT INTO dbd$indices (
         table_id
        ,name
        ,local
        ,kind
        ,uuid
    )
    VALUES (
         :table_id
        ,:name
        ,:local
        ,:kind
        ,:uuid
    )
"""

insert_index_detail = """
    INSERT INTO dbd$index_details (
         index_id
        ,position
        ,field_id
        ,expression
        ,descend
    )
    VALUES (
         :index_id
        ,:position
        ,:field_id
        ,:expression
        ,:descend
    )
"""

update_unique_key ="""
    UPDATE dbd$constraints
    SET unique_key_id = :id
"""

get_schema_id = """
    SELECT id,name FROM dbd$schemas
        WHERE name = :name
"""

get_domains_id = """
    SELECT id,name FROM dbd$domains
"""
get_fields_id = """
    SELECT id,name FROM dbd$fields
"""
get_tables_id = """
    SELECT id,name FROM dbd$tables
"""

get_schemas = """
    SELECT
         s.id
        ,s.name
        ,s.fulltext_engine
        ,s.version
        ,s.description
    FROM dbd$schemas AS s
    ORDER BY s.id
"""
get_domains ="""
    SELECT
         dom.id
        ,dom.name
        ,dom.description
        ,type.type_id    AS data_type_name
        ,dom.length
        ,dom.char_length
        ,dom.precision
        ,dom.scale
        ,dom.width
        ,dom.align
        ,dom.show_null
        ,dom.show_lead_nulls
        ,dom.thousands_separator
        ,dom.summable
        ,dom.case_sensitive
    FROM dbd$domains    AS dom
    JOIN dbd$data_types AS type
        ON dom.data_type_id = type.type_id
        ORDER BY dom.name
"""
get_tables ="""
    SELECT
         tab.id
        ,tab.schema_id
        ,tab.name
        ,tab.description
        ,tab.can_add
        ,tab.can_edit
        ,tab.can_delete
        ,tab.temporal_mode
        ,tab.means
    FROM dbd$tables  AS tab
"""

get_fields = """
    SELECT
         field.id
        ,field.table_id
        ,field.name
        ,field.russian_short_name
        ,field.description
        ,dom.name                  AS domain_name
        ,field.can_input
        ,field.can_edit
        ,field.show_in_grid
        ,field.show_in_details
        ,field.is_mean
        ,field.autocalculated
        ,field.required
    FROM dbd$fields  AS field
    JOIN dbd$domains AS dom
        ON field.domain_id = dom.id
    ORDER BY field.position
"""
get_constraints="""
   SELECT
         con.id
        ,tab.id AS table_id
        ,con.name
        ,con.constraint_type
        ,con.reference
        ,con.unique_key_id
        ,con.has_value_edit
        ,con.cascading_delete
        ,con.expression
    FROM dbd$constraints AS con
    JOIN dbd$tables  AS tab
        ON con.table_id = tab.id
"""

get_constraint_details = """
    SELECT
         detail.id
        ,detail.constraint_id
        ,field.name           AS field_name
    FROM dbd$constraint_details AS detail
    JOIN dbd$fields             AS field
        ON detail.field_id = field.id
    ORDER BY detail.position
"""
get_indices = """
    SELECT
         ind.id
        ,ind.table_id
        ,ind.name
        ,ind.local
        ,ind.kind
    FROM dbd$indices AS ind
"""
get_index_details = """
    SELECT
         detail.id
        ,detail.index_id
        ,field.name        AS field_name
        ,detail.expression
        ,detail.descend
    FROM dbd$index_details AS detail
    JOIN dbd$fields        AS field
        ON detail.field_id = field.id
    ORDER BY detail.position
"""