import ast

def parse_control_structures(code):
    """Pythonコードから制御構文を抽出し、複雑度を測定します"""
    tree = ast.parse(code)
    control_structures = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For)):
            # 制御構文の種類とネスト深さを記録
            structure = {
                'type': type(node).__name__,
                'depth': get_nesting_depth(node)
            }
            control_structures.append(structure)
    
    return control_structures

def get_nesting_depth(node):
    """制御構文のネスト深さを測定します"""
    depth = 0
    parent = node.parent
    while parent is not None:
        if isinstance(parent, (ast.If, ast.For)):
            depth += 1
        parent = parent.parent
    return depth