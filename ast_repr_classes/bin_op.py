from .base_class import BaseReprAST

class BinOp(BaseReprAST):
    total_instance = 0
    instance_storage = []
    
    def __init__(self, node, **kwags):
        self.setAttr(**kwags)
        super().__init__(**node.__dict__)
        BinOp.total_instance += 1
        BinOp.instance_storage.append(self)
