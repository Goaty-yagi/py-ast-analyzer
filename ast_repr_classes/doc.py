import ast

from .base_class import BaseReprAST

class Doc(BaseReprAST):
    total_instance = 0
    instance_storage = []
    
    def __init__(self, node, **kwags):
        self.setAttr(**kwags)
        super().__init__(**node.__dict__)
        Doc.total_instance += 1
        Doc.instance_storage.append(self)