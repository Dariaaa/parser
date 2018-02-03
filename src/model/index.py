# -*- coding: utf-8 -*-

class Index:
    def __init__(self):
        self.name = None
        self.kind = None

        self.local = False

        self.details = []


class IndexDetail:
    def __init__(self):
        self.value = None
        self.expression = None
        self.descend = None
