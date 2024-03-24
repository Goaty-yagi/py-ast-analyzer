import ast

from .base_class import BaseReprAST

class BoolOp(BaseReprAST):
    total_instance = 0
    instance_storage = []
    
    def __init__(self, node, script, **kwags):
        self.setAttr(**kwags)
        self.values_handler(script, *self.values)
        super().__init__(**node.__dict__)
        BoolOp.total_instance += 1
        BoolOp.instance_storage.append(self)

    def values_handler(self, script, *args):
        self.values = []
        for arg in args:
            self.values.append(ast.get_source_segment(script, arg))
