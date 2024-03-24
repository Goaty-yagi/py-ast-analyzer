from .base_class import BaseReprAST

class Compare(BaseReprAST):
    total_instance = 0
    instance_storage = []
    
    def __init__(self, node, script, **kwags):
        self.setAttr(**kwags)
        super().__init__(**node.__dict__)
        Compare.total_instance += 1
        Compare.instance_storage.append(self)


