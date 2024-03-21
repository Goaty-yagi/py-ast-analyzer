import ast
import os
from ast_repr import BaseReprAST, Call
from node_count_strage import NCS
"""
This module provides CustomNodeVisitor class
inherited from NodeVisitor class
"""


class CustomNodeVisitor(ast.NodeVisitor):
    """
    Custom AST NodeVisitor class for counting occurrences of specific nodes.

    Attributes:
    - script: the script to be parsed, or the path to be read and parsed.
    - __sum: Total count of nodes visited.
    - __last_node: Last node of the initial node.
    - __node_count: Dictionary to store counts of different node types.
    - __format_values: List to store format value to check specifiers.
    - __doc_list: List to store the doc dictionary according
    to __doc_d_prototype attributes.

    """
    unparser = ast._Unparser()
    __DC_list = ["ClassDef", "AsyncFunctionDef", "FunctionDef"]
    __ASSIGN_list = ["Assign", "AugAssign", "AnnAssign", "NamedExpr"]
    __OP_mapping = unparser.binop
    __COMPARE_mapping = unparser.cmpops
    __BOOL_OP_mapping = unparser.boolops
    def __init__(self, script: str) -> None:
        """
        Initializes the CustomNodeVisitor object.
        """
        self.__set_ast_tree(script)
        self.script = script
        self.__sum = 0
        self.__last_node = None
        self.__node_count = {}
        self.__format_values = []

        self.visit(self.tree)

    @property
    def sum(self) -> int:
        """
        Property method to get the value of the 'sum' attribute.

        Returns:
        - The total count of nodes visited.
        """
        return self.__sum

    @sum.setter
    def sum(self, value: any):
        """
        Setter method for 'sum' attribute, raise Attribute error.

        Parameters:
        - value(any): The value to set (ignored).

        Raises:
        - AttributeError: This attribute is read-only.
        """
        raise AttributeError(CustomNodeVisitor.__read_only_error_text("sum"))

    @property
    def node_count(self) -> int:
        """
        Property method to get the value of the 'node_count' attribute.

        Returns:
        - __node_count attribute.
        """
        return self.__node_count

    @node_count.setter
    def node_count(self, value: any):
        """
        Setter method for 'node_count' attribute, raise Attribute error.

        Parameters:
        - value(any): The value to set (ignored).

        Raises:
        - AttributeError: This attribute is read-only.
        """
        raise AttributeError(
            CustomNodeVisitor.__read_only_error_text("node_count"))

    @property
    def format_values(self) -> None:
        """
        Property method to raise ValueError for "format_values" attribute.

        Raises:
        - ValueError: Not allowed to access.
        """
        raise ValueError(
            CustomNodeVisitor.__not_allowed_error_text("format_values"))

    @format_values.setter
    def format_values(self, value: any) -> None:
        """
        Property method to raise ValueError for "format_values" attribute.

        Parameters:
        - value(any): The value to set (ignored).

        Raises:
        - ValueError: Not allowed to access.
        """
        raise ValueError(
            CustomNodeVisitor.__not_allowed_error_text("format_values"))

    @staticmethod
    def __not_allowed_error_text(attr: str) -> str:
        """
        Static method to provide error text for not allowed attribute access.

        Parameters:
        - attr(str): The attribute name.

        Returns:
        - Error message string.
        """
        return f"You are not allowed to access '{attr}' attribute."

    @staticmethod
    def __read_only_error_text(attr: str) -> str:
        """
        Staticmethod to provide error text for read_only.

        Parameters:
        - attr(str): The attribute name.

        Return:
        - Error message string.
        """
        return f"Attribute '{attr}' is read-only."

    def visit(self, node: ast.AST, *args) -> dict[str: int] | None:
        """
        Visits the given AST node and returns counts for
        a specified subset of keys, if provided.

        Parameters:
        - node: AST node to visit.
        - *args: Subset of keys to count.

        Returns:
        - None if no subset keys provided, or a dictionary
        containing counts for the specified subset keys.
        """
        super().visit(node)

    def generic_visit(self, node: ast.AST) -> None:
        """
        A generic visit method that increments
        the node count and continues the traversal.

        Parameters:
        - node: AST node to visit.
        """
        self.__count_all_node(node)
        self.__sum += 1
        super().generic_visit(node)

    def __count_all_node(self, node: ast.AST) -> None:
        node_name = node.__class__.__name__
        try:
            nc = self.__node_count[node_name]
            nc.append(node)
        except KeyError:
            self.__node_count[node_name] = (NCS(node_name, node))

    def __set_ast_tree(self, script: str) -> None:
        """
        Parse and set ast tree according to script type.
        If script is path, the script will be read and parsed to set,
        else if string, it will be parsed and set.
        """
        if os.path.exists(script):
            with open(script, 'r') as file:
                read_content = file.read()
                self.tree = ast.parse(read_content)
        else:
            self.tree = ast.parse(script)

    def dump(self, indent: int = 4) -> ast.AST:
        """
        Returns the AST dump of the script.

        Args:
        - indent (int): Number of spaces to use for indentation (default: 4).

        Returns:
        - str: AST dump of the script.
        """
        return ast.dump(self.tree, indent=indent)
    def get(self, *args: list[str]) -> dict[str: int]:
        if len(args):
            return self.get_subset(*args)
        else:
            return self.__node_count 

    def get_subset(
            self, *key_list: list[str]) -> dict[str: int]:
        """
        Returns a dictionary containing counts for
        the specified subset of keys.

        Parameters:
        - *key_list: Subset of keys to count.

        Returns:
        - Dictionary with counts for the specified keys.
        """
        return {key: self.__node_count[key] for key in self.__node_count if key in key_list}

    def format_specifier_check(self, specifier: str = ""):
        """
        Checks if a specific format specifier is present
        in any of the format values.

        Parameters:
        - node: AST node being processed.
        - specifier: Format specifier to check.

        Returns:
        - True if the specifier is present in any format value,
        False otherwise.
        """
        if specifier == '':
            raise ValueError("specifier argument is missing.")
        if len(self.__format_values):
            return any(specifier in val for val in self.__format_values)

    def __set_last_node(self, node: ast.AST) -> None:
        """
        Sets the last_node attribute to the last child node
        of the given AST node's body.

        Parameters:
        - node: AST node to determine the last child node.
        """

        # Assume that the visitation process starts with the visit method.
        self.__last_node = list(ast.iter_child_nodes(node.body[-1]))[-1]

    def get_docs(self) -> list:
        """
        This method create a list containing documemt dict, and returns it.
        """
        DC_list = self.__class__.__DC_list
        DC_list.append("Module")
        temp_list = []
        subset = self.get_subset(*DC_list)
        for key, val in subset.items():
            nodes = val.get()
            for node in nodes:
                temp_list.append({
                    "obj": node,
                    "class": key,
                    "name": node.name if not key == 'Module' else "Module",
                    "doc": ast.get_docstring(node)})
        return temp_list

    def get_call(self):
        # name = ""
        # c_type = ""
        temp_list = []
        subset: dict = self.get_subset("Call")

        for node in subset["Call"].get():
            if isinstance(node.func, ast.Attribute):
                # Handling calls to the method.
                name = node.func.attr
                c_type = "Method"
            elif isinstance(node.func, ast.Name):
                # Assuming simple function and class call.
                name = node.func.id
                def_doc_list = self.get_docs()
                c_type = "Class" if any(obj["name"] == name and isinstance(obj["obj"], ast.ClassDef)
                                        for obj in def_doc_list) else "Function"
            call_dict = {
                "type": c_type,
                "name": name,
                "s_segment": ast.get_source_segment(self.script, node),
                "args": node.args,
                "kwags": node.keywords
            }
            temp_list.append(Call(node, self.script ,**call_dict))
        return temp_list

    def get_assign(self) -> list:
        """
        Retrive all assign objs and return them in list.

        Assign: variable_name = 42
        Assign(expr* targets, expr value, string? type_comment)

        AnnAssign: variable_name: int = 42
        AugAssign(expr target, operator op, expr value)

        AugAssign: variable_name += 42
        AnnAssign(expr target, expr annotation, expr? value, int simple)

        NamedExpr: x := some_function()) > 0
        NamedExpr(expr target, expr value)
        """
        def append_obj(node:  ast.AST, key: str):
            # target and value will be sturing in future update
            t_name = ''
            t_value = ''
            if isinstance(node, ast.Assign):
                t_name = "targets"
                t_value = node.targets
            else:
                t_name = "target"
                t_value = node.target
            temp_list.append({
                "obj": node,
                "class": key,
                t_name: t_value,
                "value": node.value,
                "s_segment": ast.get_source_segment(self.script, node),
            })
        ASSIGN_list = self.__class__.__ASSIGN_list
        temp_list = []
        subset = self.get_subset(*ASSIGN_list)
        for key, val in subset.items():
            nodes = val.get()
            for node in nodes:
                if not isinstance(node, ast.Attribute):
                    append_obj(node, key)
                elif isinstance(node.ctx, ast.Store):
                    append_obj(node, key)
        return temp_list

    def get_b_op(self):
        """
        get binary operation

        BinOp(expr left, operator op, expr right)
        x + y
        """
        temp_list = []
        subset = self.get_subset("BinOp")
        for val in subset.values():
            nodes = val.get()
            for node in nodes:
                temp_list.append({
                    "obj": node,
                    "left": node.left.id if isinstance(node.left, ast.Name) else node.left.value,
                    "op": CustomNodeVisitor.__OP_mapping[node.op.__class__.__name__],
                    "right": node.right.id if isinstance(node.right, ast.Name) else node.right.value,
                    "s_segment": ast.get_source_segment(self.script, node)
                })
        return temp_list

    def get_bool_op(self):
        """
        class ast.BoolOp(op, values)
        op: class ast.And
            class ast.Or
        """
        temp_list = []
        subset = self.get_subset("BoolOp")
        for val in subset.values():
            nodes = val.get()
            for node in nodes:
                temp_list.append({
                    "obj": node,
                    "op": CustomNodeVisitor.__BOOL_OP_mapping[node.op.__class__.__name__],
                    "s_segment": ast.get_source_segment(self.script, node)
                })
        return temp_list

    def get_cmp(self):
        """
        class ast.Compare(left, ops, comparators)
        """
        temp_list = []
        subset = self.get_subset("Compare")
        for val in subset.values():
            nodes = val.get()
            for node in nodes:
                temp_list.append({
                    "obj": node,
                    "ops": node.op.__class__.__name__,
                    "s_segment": ast.get_source_segment(self.script, node)
                })
        return temp_list

    def get_compre(self):
        pass

    # *** visit_classname methods from here ***

    def visit_Module(self, node):
        """
        Visits a Module node and counts method or function calls.

        Parameters:
        - node: Module node in the AST.
        """
        if self.__last_node is None:
            self.__set_last_node(node)
        self.generic_visit(node)

    def visit_Call(self, node: ast.AST) -> None:
        """
        Visits a Call node and counts method or function calls.

        Parameters:
        - node: Call node in the AST.
        """
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == 'format':
                self.__format_values.append(node.func.value.value)
        self.generic_visit(node)


code = """
'''
return
'''
def add_numbers(a: str, b: str):
    def test():
        a = b
        a += 1
        a:int = b
        if a and b == c:
            pass
    return a + b
numbers(1,2)
print("{}, ko {%d}".format(a, b))
while(x := some_function() > 0):
    a.method(te)
    try:
        pass
    except:
        pass
class Cl:
    '''
    kookoko
    '''
    pass
myClass = Cl(1 - 2)
myClass.i = 90
func(a, b=c, *d, **e)
"""

tree = ast.parse(code, type_comments=True)
visitor = CustomNodeVisitor(code)
# print("Node_count:", visitor.get().get("Module"))
# print("Node_sum:", visitor.sum)
# print("Counts_subset:", visitor.get('While', 'import', 'BinOp'))
# print(visitor.format_specifier_check("%d"))
# print("DOCS:", visitor.get_docs())
print("CALL:", visitor.get_call())
# print()
# print("ASSIGN:", visitor.get_assign())
# print()
# print("BINARY_OP:", visitor.get_b_op())
# for i in visitor.get_assign():
#     print(ast.get_source_segment(code, i['obj']))
# print("BOOL_OP:", visitor.get_bool_op()[0]["obj"].__dict__)
# # print(visitor.dump())
# repre = BaseReprAST(**visitor.get_bool_op()[0]["obj"].__dict__)
# print(repre)