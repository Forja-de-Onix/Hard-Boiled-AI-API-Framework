from .connectors import get_connector
from .config import get_bool


def _stream_enabled(override: bool = None) -> bool:
    if override is not None:
        return override
    return get_bool("STREAM_DEFAULT", True)


async def ask(prompt: str, model: str = None, stream: bool = None, history: list = None):
    """Punto de entrada global para preguntar a la IA, sin conocer el
    proveedor activo. Devuelve un string (no-stream) o un async generator (stream).
    """
    connector = get_connector()
    messages = (history or []) + [{"role": "user", "content": prompt}]

    if _stream_enabled(stream):
        return connector.chat_stream(messages, model=model)
    return await connector.chat(messages, model=model)