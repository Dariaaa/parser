# -*- coding: utf-8 -*-


class Table:
    def __init__(self):
        self.name = None
        self.descr = None
        self.add = False
        self.edit = False
        self.delete = False
        self.temporal_mode = None
        self.means = None
        self.fields = []
        self.constraints = []
        self.indexes = []


