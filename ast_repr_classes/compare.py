import ast

from .base_class import BaseReprAST

class Compare(BaseReprAST):
    total_instance = 0
    instance_storage = []
    
    def __init__(self, node, script, **kwags):
        self.setAttr(**kwags)
        # self.ops_handler(script, *self.ops)
        super().__init__(**node.__dict__)
        Compare.total_instance += 1
        Compare.instance_storage.append(self)

    def ops_handler(self, script, *args):
        self.ops = []
        for arg in args:
            print("ARG", arg)
            self.ops.append(arg.__class__.__name__)

