class Field:
    pass

class Char(Field):
    def __init__(self, string='', **kwargs): pass

class Text(Field):
    def __init__(self, string='', **kwargs): pass

class Integer(Field):
    def __init__(self, string='', **kwargs): pass

class Float(Field):
    def __init__(self, string='', **kwargs): pass

class Boolean(Field):
    def __init__(self, string='', **kwargs): pass

class Selection(Field):
    def __init__(self, selection, string='', **kwargs): pass

class Many2one(Field):
    def __init__(self, comodel_name, string='', **kwargs): pass

class One2many(Field):
    def __init__(self, comodel_name, inverse_name, string='', **kwargs): pass

class Many2many(Field):
    def __init__(self, comodel_name, string='', **kwargs): pass

class Date(Field):
    def __init__(self, string='', **kwargs): pass

class Datetime(Field):
    def __init__(self, string='', **kwargs): pass
