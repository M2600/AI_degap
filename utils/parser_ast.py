import ast

def add_parent_info(node, parent=None):
    for child in ast.iter_child_nodes(node):
        child.parent = node
        add_parent_info(child, node)

def get_nesting_depth(node):
    depth = 0
    parent = getattr(node, 'parent', None)
    while parent is not None:
        if isinstance(parent, (ast.If, ast.For)):
            depth += 1
        parent = getattr(parent, 'parent', None)
    return depth

def parse_control_structures(code):
    """ASTを使って制御構文とネスト深さを抽出"""
    tree = ast.parse(code)
    add_parent_info(tree)
    control_structures = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For)):
            structure = {
                'type': type(node).__name__,
                'depth': get_nesting_depth(node)
            }
            control_structures.append(structure)
    return control_structures
