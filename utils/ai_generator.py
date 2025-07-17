from utils import parser_tokenize
def check_code_elements(code, required_elements, allowed_elements):
    """
    コード中の学習要素パスが条件に合致しているか判定
    - required_elements: 必ず含めるべきパス（リスト）
    - allowed_elements: 含めてもよいパス（リスト）
    Returns: (bool, dict) 合致していればTrue, 不一致内容をdictで返す
    """
    code_paths = set(parser_tokenize.tree_to_paths(parser_tokenize.parse_control_structure_tree(code)))
    required_set = set(required_elements)
    allowed_set = set(allowed_elements)
    # 必須要素がすべて含まれているか
    missing = required_set - code_paths
    # 許可されていない要素が含まれていないか
    forbidden = code_paths - required_set - allowed_set
    ok = (not missing) and (not forbidden)
    return ok, {"missing": list(missing), "forbidden": list(forbidden), "all_paths": list(code_paths)}
"""
AIによる中間プログラム生成モジュール
- 必須: 学習要素（必ず含める）
- 使用可能要素（含めてもよい）
- どちらにも含まれない要素は使わない
"""

def build_prompt(learning_elements, allowed_elements, forbidden_elements=None, language="python", extra_prompt=None):
    """
    学習要素・使用可能要素からAI用プロンプトを生成
    """
    forbidden_elements = forbidden_elements or []
    prompt = f"""
You are an AI for generating beginner-friendly {language} programming problems.
Please strictly follow these requirements:
- Required elements: {', '.join(learning_elements)}
- Allowed elements: {', '.join(allowed_elements)}
- Allowed elements do not have to be used. Prioritize simplicity.
- Forbidden elements: {', '.join(forbidden_elements) if forbidden_elements else 'None'}
- Do NOT use any forbidden elements under any circumstances.
- Generate only one simple and easy-to-understand example code.
- Output code only. Do not include any explanation or comments.
Element notes:
- 'if' means an if statement. if, elif, and else are distinct; allowing 'if' does not mean 'elif' or 'else' are allowed.
- '/' denotes nesting. For example, 'for/if' means an if statement inside a for loop. 'for/for/if' means an if statement inside two nested for loops.
- Do not assume that allowing 'for' and 'if' means 'for/if' is allowed. Only use the specified elements and nesting.
"""
    if extra_prompt:
        prompt += f"\n{extra_prompt}\n"
    return prompt

def extract_code_from_ai_response(response):
    """
    AIの出力からコード部分のみを抽出する
    - コードブロック（```python ... ```や``` ... ```）があればその中身を返す
    - なければ全体を返す
    """
    import re
    # <think> ... </think> を除去
    response = re.sub(r'<think>[\s\S]*?</think>', '', response, flags=re.IGNORECASE)
    # ```python ... ``` or ``` ... ```
    code_blocks = re.findall(r"```(?:python)?\s*([\s\S]+?)```", response)
    if code_blocks:
        return code_blocks[0].strip()
    return response.strip()
# 例: 実際のAI API呼び出し部分はダミー関数で用意

def generate_code_with_ai(learning_elements, allowed_elements, forbidden_elements=None, language="python", ai_func=None, extra_prompt=None):
    """
    AIモデルを使って中間プログラムを生成
    ai_func: 実際のAI呼び出し関数 (プロンプトを引数にとる関数)
    extra_prompt: 追加でプロンプト末尾に追記する文
    """
    prompt = build_prompt(learning_elements, allowed_elements, forbidden_elements, language, extra_prompt=extra_prompt)
    if ai_func is None:
        # ダミー: 実際はAPI呼び出し等
        return f"# AI生成コード（ダミー）\n# prompt:\n{prompt}"
    response = ai_func(prompt)
    return extract_code_from_ai_response(response)
