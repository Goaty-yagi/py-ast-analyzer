from .base_class import BaseReprAST
from .comprehension import comprehension


class Comp(BaseReprAST):
    """
    This class representing these 4 ast classes below:
        class ast.ListComp(elt, generators)
        class ast.SetComp(elt, generators)
        class ast.GeneratorExp(elt, generators)
        class ast.DictComp(key, value, generators)
    """
    total_instance = 0
    instance_storage = []

    def __init__(self, node, script, **kwags):
        self.setAttr(**kwags)
        self.generator_handler(script, *self.generators)
        super().__init__(**node.__dict__)
        Comp.total_instance += 1
        Comp.instance_storage.append(self)

    def generator_handler(self, script, *args):
        self.generators = []
        for arg in args:
            if arg:
                self.generators.append(comprehension(arg, script, **arg.__dict__))
