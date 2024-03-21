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

    def setAttr(self, **kwags) -> None:
        for key, val in kwags.items():
            setattr(self, key, val)
