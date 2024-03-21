from .base_class import BaseReprAST

class BinaryOperation(BaseReprAST):
    total_instance = 0
    instance_storage = []
    
    def __init__(self, node, **kwags):
        self.setAttr(**kwags)
        super().__init__(**node.__dict__)
        BinaryOperation.total_instance += 1
        BinaryOperation.instance_storage.append(self)
