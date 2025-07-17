from utils import parser_tokenize


def detect_multiple_new_elements(filepaths):
    """
    学習順に並んだプログラムファイルリストを受け取り、
    2つ以上新規学習要素（パス）が現れる箇所を返す
    Returns: List of (index, filepath, [new_elements])
    """
    learned = set()
    flagged = []
    for idx, path in enumerate(filepaths):
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
        tree = parser_tokenize.parse_control_structure_tree(code)
        elements = set(parser_tokenize.tree_to_paths(tree))
        new_elements = elements - learned
        if len(new_elements) >= 2:
            flagged.append((idx, path, list(new_elements)))
        learned |= elements
    return flagged
