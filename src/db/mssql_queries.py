get_schemas = """
  SELECT
         sch.schema_id   AS id
        ,sch.name        AS name
        ,NULL            AS fulltext_engine
        ,NULL            AS version
        ,NULL            AS description
    FROM sys.schemas AS sch
    ORDER BY sch.schema_id
"""
get_domains = """
SELECT
         ROW_NUMBER() OVER (
							ORDER BY
								 col.object_id
								,col.column_id
							)                    AS id
        ,col.name
			+ CAST(col.object_id AS VARCHAR(20)) AS name
        ,NULL                                    AS description
        ,type.name                               AS data_type_name
        ,col.max_length                          AS length
        ,col.max_length                          AS char_length
        ,col.precision                           AS precision
        ,col.scale                               AS scale
        ,NULL                                    AS width
        ,NULL                                    AS align
        ,NULL                                    AS show_null
        ,NULL                                    AS show_lead_nulls
        ,NULL                                    AS thousands_separator
        ,NULL                                    AS summable
        ,NULL                                    AS case_sensitive
    FROM sys.columns       AS col
	INNER JOIN sys.types   AS type
		ON col.system_type_id = type.system_type_id
		AND col.user_type_id = type.user_type_id

"""
get_tables = """
SELECT
         tab.object_id AS id
        ,tab.schema_id AS schema_id
        ,tab.name	   AS name
        ,NULL          AS description
        ,NULL          AS can_add
        ,NULL          AS can_edit
        ,NULL          AS can_delete
        ,NULL          AS temporal_mode
        ,NULL          AS means
    FROM sys.tables    AS tab
"""
get_fields = """
SELECT
         ROW_NUMBER() OVER (
							ORDER BY
								 field.object_id
								,field.column_id
							)                         AS id
        ,field.object_id                              AS table_id
        ,field.name                                   AS name
        ,field.collation_name                         AS russian_short_name
        ,NULL                                         AS description
        ,field.name
			+ CAST(field.object_id AS VARCHAR(20))    AS domain_name
        ,NULL                                         AS can_input
        ,NULL                                         AS can_edit
        ,NULL                                         AS show_in_grid
        ,NULL                                         AS show_in_details
        ,NULL                                         AS is_mean
        ,field.is_computed                            AS autocalculated
        ,NULL                                         AS required
    FROM sys.columns                                  AS field
    ORDER BY field.column_id

"""
get_constraints = """
 SELECT
         con.object_id        AS id
        ,con.parent_object_id AS table_id
        ,con.name			  AS name
        ,'PRIMARY'            AS constraint_type
        ,NULL                 AS reference
        ,NULL                 AS unique_key_id
        ,NULL                 AS has_value_edit
        ,NULL                 AS cascading_delete
        ,NULL                 AS expression
    FROM sys.objects          AS con
    WHERE con.type = 'PK'
    UNION ALL
    SELECT
         con.object_id                         AS id
        ,con.parent_object_id                  AS table_id
        ,con.name			                   AS name
        ,'FOREIGN'                             AS constraint_type
        ,OBJECT_NAME(con.referenced_object_id) AS reference
        ,NULL                                  AS unique_key_id
        ,NULL                                  AS has_value_edit
        ,NULL                                  AS cascading_delete
        ,NULL                                  AS expression
    FROM sys.foreign_keys AS con
    """
get_constraint_details = """
SELECT
         ROW_NUMBER() OVER (
							ORDER BY
								 det.constraint_id
								,det.field_name
							) AS id
        ,det.constraint_id		                    AS constraint_id
        ,det.field_name                             AS field_name
    FROM (
		SELECT
			 con.object_id   AS constraint_id
			,det.COLUMN_NAME AS field_name
		FROM sys.objects								      AS con
		INNER JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS det
			ON con.name = det.CONSTRAINT_NAME
		WHERE con.type = 'PK'
		UNION ALL
		SELECT
			 con.object_id                                      AS constraint_id
			,COL_NAME(det.parent_object_id, det.parent_column_id) AS field_name
		FROM sys.foreign_keys              AS con
		INNER JOIN sys.foreign_key_columns AS det
			ON con.object_id = det.constraint_object_id
	) AS det
"""
get_indices = """
 SELECT
         ROW_NUMBER() OVER (
							ORDER BY
								 ind.object_id
								,ind.index_id
							)                         AS id
        ,ind.object_id                                AS table_id
        ,ind.name                                     AS name
        ,NULL                                         AS local
        ,CASE
			WHEN ind.is_unique = 1
				THEN 'uniqueness'
			ELSE NULL
         END AS kind
    FROM sys.indexes AS ind
"""
get_index_details = """
 SELECT
         ROW_NUMBER() OVER(
							    ORDER BY
								 detail.object_id
								,detail.index_id
							 )                            AS id
        ,ind.id                                           AS index_id
        ,col.name                                         AS field_name
        ,NULL							                  AS expression
        ,detail.is_descending_key                         AS descend
    FROM
	(
		SELECT
			ROW_NUMBER() OVER(
							    ORDER BY
								 ind.object_id
								,ind.index_id
							 )                            AS id
			,ind.object_id                                AS table_id
			,ind.index_id                                 AS index_id
			,ind.name
		FROM sys.indexes   AS ind
    )                      AS ind
	JOIN sys.index_columns AS detail
		ON detail.object_id = ind.table_id
		AND detail.index_id = ind.index_id
	INNER JOIN sys.columns AS col
		ON detail.column_id = col.column_id
		AND detail.object_id = col.object_id
    ORDER BY detail.column_id
"""