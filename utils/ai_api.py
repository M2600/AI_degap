"""
AI API実行モジュール（Ollama用・拡張性あり）
今後ChatGPT, Gemini, Claude等にも対応しやすい設計
"""
import requests

class BaseAIClient:
    def generate(self, prompt, **kwargs):
        """
        AIモデルにプロンプトを送信し、生成結果を返す
        Args:
            prompt (str): 生成用プロンプト
            **kwargs: モデルごとの追加パラメータ
        Returns:
            str: 生成されたテキスト
        """
        raise NotImplementedError("generate() must be implemented by subclasses")

class OllamaClient(BaseAIClient):
    def __init__(self, base_url="http://localhost:11434", model="llama3"):
        """
        Args:
            base_url (str): Ollama APIのベースURL
            model (str): 使用するモデル名
        """
        self.base_url = base_url
        self.model = model

    def generate(self, prompt, **kwargs):
        """
        Ollama APIでテキスト生成を行う
        Args:
            prompt (str): 生成用プロンプト
            **kwargs: APIに渡す追加パラメータ
        Returns:
            str: 生成されたテキスト
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        payload.update(kwargs)
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")

# 今後の拡張例:
# class ChatGPTClient(BaseAIClient): ...
# class GeminiClient(BaseAIClient): ...
# class ClaudeClient(BaseAIClient): ...

def get_ai_client(name="ollama", **kwargs):
    """
    指定名のAIクライアントインスタンスを返す
    Args:
        name (str): "ollama"などクライアント名
        **kwargs: クライアントの初期化引数
    Returns:
        BaseAIClient: AIクライアントインスタンス
    """
    if name == "ollama":
        return OllamaClient(**kwargs)
    # elif name == "chatgpt":
    #     return ChatGPTClient(**kwargs)
    # ...
    raise ValueError(f"Unknown AI client: {name}")
