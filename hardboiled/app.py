import asyncio
import json
import socket
from .router import Router



class Request:
    def __init__(self, method, path, headers, body, params=None, query=None):
        self.method = method
        self.path = path
        self.headers = headers
        self.body = body
        self.params = params or {}
        self.query = query or {}

    def json(self):
        return json.loads(self.body or "{}")

    async def _handle_client(self, reader, writer):
        sock = writer.get_extra_info("socket")
        if sock is not None:
            sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        try:
            request = await self._parse_request(reader)
            response = await self._dispatch(request)
            await response.render(writer)
        except Exception:
            writer.write(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
        finally:
            writer.close()
            await writer.wait_closed()

    async def _serve(self, host: str, port: int):
        server = await asyncio.start_server(self._handle_client, host, port)
        addr = server.sockets[0].getsockname()
        print(f"Hard Boiled escuchando en http://{addr[0]}:{addr[1]}")
        async with server:
            await server.serve_forever()

    def listen(self, port: int = 3000, host: str = "127.0.0.1"):
        asyncio.run(self._serve(host, port))


class Response:
    def __init__(self):
        self.status_code = 200
        self.headers = {"Content-Type": "text/plain; charset=utf-8"}
        self._body = b""
        self._stream_gen = None

    def status(self, code: int):
        self.status_code = code
        return self

    def set_header(self, key, value):
        self.headers[key] = value
        return self

    def text(self, content: str):
        self.headers["Content-Type"] = "text/plain; charset=utf-8"
        self._body = content.encode("utf-8")
        return self

    def json(self, data):
        self.headers["Content-Type"] = "application/json; charset=utf-8"
        self._body = json.dumps(data).encode("utf-8")
        return self

    def stream(self, async_generator):
        self._stream_gen = async_generator
        self.headers["Transfer-Encoding"] = "chunked"
        return self

    async def render(self, writer: asyncio.StreamWriter):
        writer.write(f"HTTP/1.1 {self.status_code} OK\r\n".encode())

        if self._stream_gen is not None:
            headers = dict(self.headers)
            headers.pop("Content-Length", None)
            for k, v in headers.items():
                writer.write(f"{k}: {v}\r\n".encode())
            writer.write(b"\r\n")
            async for chunk in self._stream_gen:
                if isinstance(chunk, str):
                    chunk = chunk.encode("utf-8")
                writer.write(f"{len(chunk):x}\r\n".encode())
                writer.write(chunk + b"\r\n")
                await writer.drain()
            writer.write(b"0\r\n\r\n")
        else:
            self.headers["Content-Length"] = str(len(self._body))
            for k, v in self.headers.items():
                writer.write(f"{k}: {v}\r\n".encode())
            writer.write(b"\r\n")
            writer.write(self._body)

        await writer.drain()


class App:
    def __init__(self):
        self.router = Router()
        self.middlewares = []

    def use(self, middleware):
        self.middlewares.append(middleware)

    def get(self, path):
        return self.router.get(path)

    def post(self, path):
        return self.router.post(path)

    def put(self, path):
        return self.router.put(path)

    def delete(self, path):
        return self.router.delete(path)

    async def _parse_request(self, reader: asyncio.StreamReader) -> Request:
        request_line = await reader.readline()
        method, raw_path, _ = request_line.decode().strip().split(" ")

        path, _, query_string = raw_path.partition("?")
        query = {}
        for pair in query_string.split("&"):
            if "=" in pair:
                k, v = pair.split("=", 1)
                query[k] = v

        headers = {}
        while True:
            line = await reader.readline()
            if line in (b"\r\n", b""):
                break
            key, value = line.decode().split(":", 1)
            headers[key.strip().lower()] = value.strip()

        body = ""
        content_length = int(headers.get("content-length", 0))
        if content_length:
            raw_body = await reader.readexactly(content_length)
            body = raw_body.decode()

        return Request(method, path, headers, body, query=query)

    async def _dispatch(self, request: Request) -> Response:
        handler, params = self.router.resolve(request.method, request.path)
        response = Response()

        if handler is None:
            return response.status(404).json({"error": "Not Found"})

        request.params = params

        async def call_handler():
            return await handler(request, response)

        chain = call_handler
        for middleware in reversed(self.middlewares):
            chain = self._wrap(middleware, request, response, chain)

        try:
            await chain()
        except Exception as exc:
            response.status(500).json({"error": str(exc)})

        return response

    def _wrap(self, middleware, request, response, next_fn):
        async def wrapped():
            await middleware(request, response, next_fn)
        return wrapped

    async def _handle_client(self, reader, writer):
        try:
            request = await self._parse_request(reader)
            response = await self._dispatch(request)
            await response.render(writer)
        except Exception:
            writer.write(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
        finally:
            writer.close()
            await writer.wait_closed()

    async def _serve(self, host: str, port: int):
        server = await asyncio.start_server(self._handle_client, host, port)
        addr = server.sockets[0].getsockname()
        print(f"Hard Boiled escuchando en http://{addr[0]}:{addr[1]}")
        async with server:
            await server.serve_forever()

    def listen(self, port: int = 3000, host: str = "127.0.0.1"):
        asyncio.run(self._serve(host, port))