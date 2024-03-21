import ast
"""
This module provides BaseReprAST class which desied for simplifying
AST attribute.
"""

class BaseReprAST:
    """
    This class is BaseClass of other specific class. This class is designed for
    common dunder methods which subclass of this class will inherited from.
    """
    def __init__(self, **kwags):
        default_args = ["lineno", "col_offset", "end_lineno", "end_col_offset"]
        for key, val in kwags.items():
            if key in default_args:
                setattr(self, key, val)

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return str(self.__dict__)


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

    def setAttr(self, **kwags) -> None:
        for key, val in kwags.items():
            setattr(self, key, val)

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
