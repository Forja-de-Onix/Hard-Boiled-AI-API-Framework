import os
import json
import httpx


class AIConnector:
    """Clase base: define la interfaz común y la configuración compartida.
    Cada proveedor hereda de aquí y solo implementa chat() / chat_stream().
    """

    def __init__(self):
        self.default_model = self._get_default_model()

    def _get_default_model(self) -> str:
        raise NotImplementedError

    async def chat(self, messages: list, model: str = None) -> str:
        raise NotImplementedError

    async def chat_stream(self, messages: list, model: str = None):
        raise NotImplementedError
        yield  # pragma: no cover


class OllamaConnector(AIConnector):
    def __init__(self):
        self.host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        super().__init__()

    def _get_default_model(self) -> str:
        return os.environ.get("OLLAMA_DEFAULT_MODEL", "llama3")

    async def chat_stream(self, messages: list, model: str = None):
        model = model or self.default_model
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                f"{self.host}/api/chat",
                json={"model": model, "messages": messages, "stream": True},
            ) as response:
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    chunk = json.loads(line)
                    content = chunk.get("message", {}).get("content", "")
                    if content:
                        yield content
                    if chunk.get("done"):
                        break

    async def chat(self, messages: list, model: str = None) -> str:
        model = model or self.default_model
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(
                f"{self.host}/api/chat",
                json={"model": model, "messages": messages, "stream": False},
            )
            data = response.json()
            return data.get("message", {}).get("content", "")


class ClaudeConnector(AIConnector):
    API_URL = "https://api.anthropic.com/v1/messages"
    API_VERSION = "2023-06-01"

    def __init__(self):
        self.api_key = os.environ.get("CLAUDE_API_KEY")
        self.max_tokens = int(os.environ.get("CLAUDE_MAX_TOKENS", "1024"))
        super().__init__()

    def _get_default_model(self) -> str:
        return os.environ.get("CLAUDE_DEFAULT_MODEL", "claude-sonnet-4-5")

    def _headers(self) -> dict:
        return {
            "x-api-key": self.api_key,
            "anthropic-version": self.API_VERSION,
            "content-type": "application/json",
        }

    async def chat(self, messages: list, model: str = None) -> str:
        model = model or self.default_model
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(
                self.API_URL,
                headers=self._headers(),
                json={"model": model, "max_tokens": self.max_tokens, "messages": messages},
            )
            data = response.json()
            blocks = data.get("content", [])
            return "".join(b.get("text", "") for b in blocks if b.get("type") == "text")

    async def chat_stream(self, messages: list, model: str = None):
        model = model or self.default_model
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                self.API_URL,
                headers=self._headers(),
                json={"model": model, "max_tokens": self.max_tokens, "messages": messages, "stream": True},
            ) as response:
                async for line in response.aiter_lines():
                    if not line or not line.startswith("data:"):
                        continue
                    payload = line[len("data:"):].strip()
                    if not payload:
                        continue
                    event = json.loads(payload)
                    if event.get("type") == "content_block_delta":
                        text = event.get("delta", {}).get("text", "")
                        if text:
                            yield text
                    elif event.get("type") == "message_stop":
                        break


class GeminiConnector(AIConnector):
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"

    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        super().__init__()

    def _get_default_model(self) -> str:
        return os.environ.get("GEMINI_DEFAULT_MODEL", "gemini-2.5-flash")

    @staticmethod
    def _to_gemini_contents(messages: list) -> list:
        role_map = {"assistant": "model", "user": "user", "system": "user"}
        return [
            {"role": role_map.get(m["role"], "user"), "parts": [{"text": m["content"]}]}
            for m in messages
        ]

    async def chat(self, messages: list, model: str = None) -> str:
        model = model or self.default_model
        url = f"{self.BASE_URL}/{model}:generateContent?key={self.api_key}"
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(url, json={"contents": self._to_gemini_contents(messages)})
            data = response.json()
            candidates = data.get("candidates", [])
            if not candidates:
                return ""
            parts = candidates[0].get("content", {}).get("parts", [])
            return "".join(p.get("text", "") for p in parts)

    async def chat_stream(self, messages: list, model: str = None):
        model = model or self.default_model
        url = f"{self.BASE_URL}/{model}:streamGenerateContent?alt=sse&key={self.api_key}"
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST", url, json={"contents": self._to_gemini_contents(messages)}
            ) as response:
                async for line in response.aiter_lines():
                    if not line or not line.startswith("data:"):
                        continue
                    payload = line[len("data:"):].strip()
                    if not payload:
                        continue
                    event = json.loads(payload)
                    candidates = event.get("candidates", [])
                    if not candidates:
                        continue
                    parts = candidates[0].get("content", {}).get("parts", [])
                    text = "".join(p.get("text", "") for p in parts)
                    if text:
                        yield text


class ChatGPTConnector(AIConnector):
    API_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        super().__init__()

    def _get_default_model(self) -> str:
        return os.environ.get("OPENAI_DEFAULT_MODEL", "gpt-4o")

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def chat(self, messages: list, model: str = None) -> str:
        model = model or self.default_model
        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(
                self.API_URL,
                headers=self._headers(),
                json={"model": model, "messages": messages, "stream": False},
            )
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def chat_stream(self, messages: list, model: str = None):
        model = model or self.default_model
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream(
                "POST",
                self.API_URL,
                headers=self._headers(),
                json={"model": model, "messages": messages, "stream": True},
            ) as response:
                async for line in response.aiter_lines():
                    if not line or not line.startswith("data:"):
                        continue
                    payload = line[len("data:"):].strip()
                    if payload == "[DONE]":
                        break
                    event = json.loads(payload)
                    delta = event["choices"][0].get("delta", {})
                    text = delta.get("content", "")
                    if text:
                        yield text


_CONNECTORS = {
    "ollama": OllamaConnector,
    "claude": ClaudeConnector,
    "gemini": GeminiConnector,
    "chatgpt": ChatGPTConnector,
}


def get_connector() -> AIConnector:
    """Resuelve el conector activo según AI_CONNECTOR en .env"""
    name = os.environ.get("AI_CONNECTOR", "ollama").lower()
    connector_cls = _CONNECTORS.get(name)
    if connector_cls is None:
        raise ValueError(f"AI_CONNECTOR desconocido: '{name}'")
    return connector_cls()