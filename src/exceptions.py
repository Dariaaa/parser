class ParseError(Exception):
    def __init__(self, mess, methodName):
        print("Parse error in " + methodName +
              " with message: " + mess)
    pass


