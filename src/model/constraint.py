# -*- coding: utf-8 -*-


class Constraint:
    def __init__(self):
        self.name = None
        self.kind = None
        self.items = None
        self.reference_type = None
        self.reference = None
        self.has_value_edit = False
        self.cascading_delete = False
        self.full_cascading_delete = False