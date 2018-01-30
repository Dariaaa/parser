
add_schema_sql = "INSERT INTO dbd$schemas (name) VALUES ('{}')"

add_domains_sql = """INSERT INTO dbd$domains (
        name,
        description,
        length,
        char_length,
        precision,
        scale,
        width,
        align,
        show_null,
        show_lead_nulls,
        thousands_separator,
        summable,
        case_sensitive,
        data_type_id,
        uuid)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

update_rel_domain_datatype = """
        UPDATE dbd$domains
        SET data_type_id = (
        SELECT dbd$data_types.id
        FROM dbd$domains as dom
        JOIN dbd$tmpdatatype
        ON dbd$domains.name = dbd$tmpdatatype.domain_name
        JOIN dbd$data_types
        ON dbd$tmpdatatype.datatype_name = dbd$data_types.type_id
        WHERE dom.name = name)
        """

add_temp_table_sql = """CREATE TABLE dbd$tmpdatatype
(domain_name varchar NOT NULL, datatype_name varchar NOT NULL)"""

fill_temp_table_sql ="INSERT INTO dbd$tmpdatatype VALUES(?, ?)"

drop_temp_table_sql = "DROP TABLE dbd$tmpdatatype"

