import ast

from .base_class import BaseReprAST


class Call(BaseReprAST):
    total_instance = 0
    instance_storage = []

    def __init__(self, node, script, **kwags):
        self.setAttr(**kwags)
        self.args_handler(script, *self.args)
        self.kwags_handler(script, *self.kwags)
        super().__init__(**node.__dict__)
        Call.total_instance += 1
        Call.instance_storage.append(self)

    def args_handler(self, script, *args) -> None:
        self.args = []
        for arg in args:
            self.args.append(ast.get_source_segment(script, arg))

    def kwags_handler(self, script, *args) -> None:
        self.kwags = []
        for arg in args:
            self.kwags.append(ast.get_source_segment(script, arg))

    @classmethod
    def print(cls) -> None:
        for i in Call.instance_storage:
            print(i)
