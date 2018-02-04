# -*- coding: utf-8 -*-

class Schema:
    def __init__(self):
        self.fulltext_engine = None
        self.version = None
        self.name = None
        self.descr = None
        self.domains = []
        self.tables = []

class Domain:
    def __init__(self):
        self.name = None
        self.descr = None
        self.type = None
        self.align = None
        self.width = None
        self.precision = None
        self.show_null = False
        self.summable = False
        self.case_sensitive = False
        self.show_lead_nulls = False
        self.thousands_separator = False
        self.char_length = None
        self.length = None
        self.scale = None

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

class Field:
    def __init__(self):
        self.name = None
        self.rname = None
        self.domain = None
        self.descr = None
        self.input = False
        self.edit = False
        self.show_in_grid = False
        self.show_in_details = False
        self.is_mean = False
        self.autocalculated = False
        self.required = False

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

class Constraint:
    def __init__(self):
        self.name = None
        self.kind = None
        self.items = None
        self.expression = None
        self.reference = None
        self.has_value_edit = False
        self.cascading_delete = None

        self.details = []

class ConstraintDetail:
    def __init__(self):
        self.value = None