from utils.exceptions import TypeNotFoundException


def get_type_in_postgres(domain):
    """
    Get type of domain in postgresql
    :param domain:
    :return:
    """
    if domain.type.lower() in ['uniqueidentifier', 'money', 'sql_variant', 'bit']:
        return 'varchar(200)'
    elif domain.type.lower() in ['ntext', 'nchar', 'char', 'blob', 'varbinary', 'binary', 'image']:
        return 'text'
    elif domain.type.lower() in ['boolean','date','time']:
        return domain.type.lower()
    elif domain.type.lower() in ['largeint', 'code', 'bigint']:
        return 'bigint'
    elif domain.type.lower() in ['word', 'byte', 'smallint', 'int', 'tinyint']:
        return 'integer'
    elif domain.type.lower() in ['float', 'real']:
        return 'real'
    elif domain.type.lower() in ['datetime','datetimeoffset']:
        return 'timestamp'
    elif domain.type.lower() in ['string', 'memo', 'sysname', 'nvarchar', 'varchar']:
        if domain.char_length and int(domain.char_length) > 0:
            return """ {} ({})""".format('varchar',domain.char_length)
        else:
            return 'varchar'
    print(domain.type)
    raise TypeNotFoundException(domain.type)
