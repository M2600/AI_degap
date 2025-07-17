CONTROL_ELEMENTS = [
    'if', 'elif', 'else', 'for', 'break', 'continue'
    # 必要に応じて他の要素も追加
]
import sys
from utils import parser_tokenize
from utils import gap_detector
from utils import ai_generator
from utils import ai_api
import glob

def analyze_program_file(filepath):
    """指定したPythonファイルをparser_tokenize.pyで分析し、制御構文情報を返す"""
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    return parser_tokenize.parse_control_structures(code)

def analyze_program_file_paths(filepath):
    """指定したPythonファイルをparser_tokenize.pyで分析し、パス形式で制御構文を返す"""
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    tree = parser_tokenize.parse_control_structure_tree(code)
    return parser_tokenize.tree_to_paths(tree)



def detect_gaps_cli():
    """ギャップ検出CLI処理"""
    filepaths = sorted(glob.glob("sample/*.py"))
    learned = set()
    for idx, path in enumerate(filepaths):
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
        tree = parser_tokenize.parse_control_structure_tree(code)
        elements = set(parser_tokenize.tree_to_paths(tree))
        new_elements = elements - learned

        print(f"{idx+1}: {path} 新規学習要素数: {len(new_elements)} 新規要素: {list(new_elements)}")
        learned |= elements


def generate_code_cli(args):
    """AIコード生成CLI処理"""
    # 例: --generate-code for/if --allow else,elif --forbid break,continue
    if len(args) < 1:
        print("Usage: python main.py --generate-code <learning_elements(,区切り)> [--allow <allowed_elements(,区切り)>] [--forbid <forbidden_elements(,区切り)>]")
        sys.exit(1)
    learning_elements = [e.strip() for e in args[0].split(",") if e.strip()]
    allowed_elements = []
    forbidden_elements = None  # Noneで未指定を区別
    idx = 1
    while idx < len(args):
        if args[idx] == "--allow" and idx+1 < len(args):
            allowed_elements = [e.strip() for e in args[idx+1].split(",") if e.strip()]
            idx += 2
        elif args[idx] == "--forbid" and idx+1 < len(args):
            forbidden_elements = [e.strip() for e in args[idx+1].split(",") if e.strip()]
            idx += 2
        else:
            idx += 1
    # forbidden_elements未指定時はデフォルトでCONTROL_ELEMENTSから必須・許可要素を除いたもの
    if forbidden_elements is None:
        forbidden_elements = [e for e in CONTROL_ELEMENTS if e not in learning_elements and e not in allowed_elements]
    # デバッグ出力
    print(f"[DEBUG] learning_elements: {learning_elements}")
    print(f"[DEBUG] allowed_elements: {allowed_elements}")
    print(f"[DEBUG] forbidden_elements: {forbidden_elements}")
    # AIクライアント取得（Ollama前提）
    client = ai_api.get_ai_client("ollama", model="qwen3:14b")
    def ai_func(prompt):
        return client.generate(prompt)
    max_retry = 3
    prompt_reason = ""
    for attempt in range(1, max_retry+1):
        code = ai_generator.generate_code_with_ai(learning_elements, allowed_elements, forbidden_elements, ai_func=ai_func, extra_prompt=prompt_reason)
        print(f"=====[Generated code attempt {attempt}]=====")
        print(code)
        print("==========================")
        ok, info = ai_generator.check_code_elements(code, learning_elements, allowed_elements)
        forbidden_used = info.get('forbidden', []) if info else []
        missing = info.get('missing', []) if info else []
        if ok and not forbidden_used:
            print("Code meets the requirements.")
            break
        else:
            print("Code does not meet the requirements:")
            print(f"Missing elements: {missing}")
            print(f"Forbidden elements: {forbidden_used}")
            print(f"All paths in code: {info['all_paths'] if info else ''}")
            # 理由をプロンプトに追記
            reasons = []
            if forbidden_used:
                reasons.append(f"The following elements must NOT be used: {', '.join(forbidden_used)}.")
            if missing:
                reasons.append(f"The following elements MUST be used: {', '.join(missing)}.")
            if reasons:
                prompt_reason = "\n[Note for AI] Previous output was rejected for the following reasons: " + " ".join(reasons) + " Please strictly follow the requirements."
            else:
                prompt_reason = ""
    else:
        print("Failed to generate code that meets the requirements after multiple attempts.")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--detect-gaps":
        detect_gaps_cli()
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--generate-code":
        generate_code_cli(sys.argv[2:])
        return

    filepath = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[2] == "--paths":
        result = analyze_program_file_paths(filepath)
        print("\n".join(result))
    else:
        result = analyze_program_file(filepath)
        print(result)

if __name__ == "__main__":
    main()


