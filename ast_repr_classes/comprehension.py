import ast

from .base_class import BaseReprAST

class comprehension(BaseReprAST):
    """
    This class represent comprehension class
    class ast.comprehension(target, iter, ifs, is_async)
    """
    total_instance = 0
    instance_storage = []
    
    def __init__(self, node, script, **kwags):
        self.setAttr(script, **kwags)
        comprehension.total_instance += 1
        comprehension.instance_storage.append(self)

    def setAttr(self, script, **kwags):
        for key, val in kwags.items():
            if isinstance(val, ast.AST):
                setattr(self, key, ast.get_source_segment(script, val))
            elif isinstance(val, list) and len(val):
                temp_list = []
                for i in val:
                    temp_list.append(ast.get_source_segment(script, i))
                setattr(self, key, temp_list)
            else:
                setattr(self, key, val)
