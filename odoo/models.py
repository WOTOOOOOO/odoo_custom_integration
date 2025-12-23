class Model:
    _name = ''
    _inherit = ''
    _description = ''
    
    def ensure_one(self): pass
    def write(self, vals): pass
    def message_post(self, body='', **kwargs): pass
    def search(self, domain): return []
    def browse(self, ids): return []
    def create(self, vals): return self
    def unlink(self): pass
