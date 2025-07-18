
# AI_degap プロジェクト概要

## プロジェクト説明
AI_degapは、Pythonサンプルプログラム群の「制御構造のギャップ」を検出し、AIを用いてギャップを埋める中間難易度のプログラムを自動生成・保存するツールです。

- サンプルプログラム（sample/*.py）を解析し、制御構造（if, else, for等）の新規要素（ギャップ）を検出
- ギャップが2以上の場合、AI（Ollama/Qwen3モデル）で新規要素ごとに中間プログラムを生成
- 生成プログラムは result/ ディレクトリに保存され、条件判定結果も出力

## 各主要プログラムの説明

- main.py
    - コマンドラインから各機能を実行するメインスクリプト
    - 機能：ギャップ検出、AIコード生成、ギャップ埋め（degap）
- utils/
    - parser_tokenize.py: Pythonコードの制御構造解析
    - ai_generator.py: AIによるコード生成・判定
    - ai_api.py: AIクライアント（Ollama）管理
    - gap_detector.py, parser.py: 補助解析
- sample/
    - 01.py ~ 13.py: 学習用サンプルプログラム
- result/
    - *_prevN.py: degap実行時に生成される中間プログラム

## 実行方法

1. 必要なPythonパッケージ・Ollama環境をセットアップしてください。
2. コマンドラインから以下のように実行します。

### ギャップ検出
```
python main.py --detect-gaps
```
- sample/*.pyの制御構造ギャップを一覧表示します。

### AIによるコード生成
```
python main.py --generate-code <要素(,区切り)> [--allow <許可要素(,区切り)>] [--forbid <禁止要素(,区切り)>]
```
- 例: `python main.py --generate-code for/if --allow else,elif --forbid break,continue`

### ギャップ埋め（degap）
```
python main.py --degap
```
- サンプル間のギャップが2以上の場合、自動で中間プログラムを生成しresult/に保存します。
- 実行後、ギャップ検出結果・生成プログラムの判定結果が表示されます。

## 注意事項
- AI生成にはOllama（Qwen3モデル）が必要です。
- result/ディレクトリはdegap実行時に自動初期化されます。
- サンプルプログラムはsample/ディレクトリに配置してください。
