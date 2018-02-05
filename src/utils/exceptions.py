class ParseError(Exception):
    def __init__(self, mess, obj):
        print("Parse error in " + obj.__name__ +
              " with message: " + mess)
    pass



