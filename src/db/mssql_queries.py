get_tables = """
select 
            t.name, 
            OBJECTPROPERTY(t.object_id, 'HasInsertTrigger') as addition, 
            OBJECTPROPERTY(t.object_id, 'HasUpdateTrigger') as edition, 
            t.temporal_type
        from sys.tables as t
        join sys.schemas as s
        on t.schema_id = s.schema_id
        where s.name = ?
"""
get_fields = """
 select 
            COLUMN_NAME as name, 
            t.name as dom,
            ORDINAL_POSITION as position, 
            sc.is_identity as edit,
            sc.is_hidden as show_in_grid,
            sc.is_computed as autocalculated,
            sc.is_nullable as required,
            col.DATA_TYPE,
            sc.scale,
            sc.precision,
            sc.max_length
        from INFORMATION_SCHEMA.TABLES as tbl
        left join INFORMATION_SCHEMA.COLUMNS as col
        on col.TABLE_NAME = tbl.TABLE_NAME
        left join sys.columns as sc
        on sc.object_id = object_id(tbl.table_schema + '.' + tbl.table_name) and sc.NAME = col.COLUMN_NAME
        left join sys.types as t
        on col.DATA_TYPE = t.name
        where tbl.TABLE_NAME = ?;
"""
get_primary_keys = """
 select 
            kc.name, 
            KCU.COLUMN_NAME as items, 
            kc.unique_index_id as unique_key_index
        from sys.tables as t
        join sys.key_constraints as kc
        on t.object_id = kc.parent_object_id
        join INFORMATION_SCHEMA.KEY_COLUMN_USAGE as KCU
        on KCU.CONSTRAINT_NAME = kc.name
        where t.object_id = object_id(?);
"""
get_foreign_keys = """
 select 
            fk.name as name, 
            ac.name as items, 
            tt.name as reference, 
            fk.delete_referential_action as cascading_delete
        from sys.tables as t
        join sys.all_columns as ac
        on t.object_id = ac.object_id
        join sys.foreign_key_columns as fkc
        on ac.column_id = fkc.parent_column_id and t.object_id = fkc.parent_object_id
        join sys.foreign_keys as fk
        on fkc.constraint_object_id = fk.object_id
        join sys.tables as tt
        on tt.object_id = fk.referenced_object_id
        where t.object_id = object_id(?);
"""
get_indices = """
 select 
            ind.name as index_name, 
            ind.is_unique, 
            fti.object_id as is_fulltext, 
            c.name as field_name
        from sys.indexes as ind
        left join sys.fulltext_indexes as fti
        on ind.object_id = fti.object_id
        join sys.index_columns as ic
        on ind.object_id = ic.object_id and ind.index_id = ic.index_id
        join sys.columns as c
        on ind.object_id = c.object_id and ic.column_id = c.column_id
        where ind.object_id = OBJECT_ID(?);
"""

