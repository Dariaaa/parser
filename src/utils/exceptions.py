class ParseError(Exception):
    def __init__(self, mess, obj):
        print("Parse error in {} with message : {} ".format(obj,mess))
    pass
class TypeNotFoundException(Exception):
    def __init__(self, type_item):
        print("Type {} not found".format(type_item))
    pass
class ItemNotFoundException(Exception):
    def __init__(self, item, obj):
        print("Items: {} in {} not found ".format(item,obj))
    pass



