
import tokenize
import io
import sys
import importlib.util

# main.pyのCONTROL_ELEMENTSを参照
def get_control_elements():
    spec = importlib.util.find_spec('main')
    if spec is not None:
        main_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_mod)
        return set(main_mod.CONTROL_ELEMENTS)
    # fallback
    return {'if', 'elif', 'else', 'for'}


def parse_control_structure_tree(code):
    """tokenizeを使ってif, elif, else, forのネスト構造をツリーとして抽出"""
    import collections
    tokens = tokenize.tokenize(io.BytesIO(code.encode('utf-8')).readline)
    root = []  # 最上位のノードリスト
    stack = [(root, -1)]  # (現在のノードリスト, インデントレベル)
    control_keywords = get_control_elements()
    for token in tokens:
        if token.type == tokenize.INDENT:
            # 新しいブロックに入る
            stack.append((stack[-1][0][-1]['children'], token.start[1]))
        elif token.type == tokenize.DEDENT:
            # ブロックを抜ける
            if len(stack) > 1:
                stack.pop()
        elif token.type == tokenize.NAME and token.string in control_keywords:
            node = {'type': token.string, 'children': []}
            stack[-1][0].append(node)
    return root

def tree_to_paths(tree, prefix=None):
    """ツリー構造からパス形式（for/if/elseなど）リストを生成"""
    if prefix is None:
        prefix = []
    paths = []
    for node in tree:
        current_path = prefix + [node['type']]
        paths.append('/'.join(current_path))
        if node['children']:
            paths.extend(tree_to_paths(node['children'], current_path))
    return paths

# 既存の関数も維持（深さ情報のみ欲しい場合用）
def parse_control_structures(code):
    """tokenizeを使ってif, elif, else, forの制御構文とネスト深さを抽出"""
    control_structures = []
    current_depth = 0
    indent_levels = []
    tokens = tokenize.tokenize(io.BytesIO(code.encode('utf-8')).readline)
    control_keywords = get_control_elements()
    for token in tokens:
        if token.type == tokenize.INDENT:
            current_depth += 1
            indent_levels.append(token.start[1])
        elif token.type == tokenize.DEDENT:
            current_depth = max(0, current_depth - 1)
            if indent_levels:
                indent_levels.pop()
        elif token.type == tokenize.NAME and token.string in control_keywords:
            control_structures.append({
                'type': token.string,
                'depth': current_depth
            })
    return control_structures
