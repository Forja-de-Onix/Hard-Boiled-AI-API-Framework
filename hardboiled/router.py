import re
from typing import Callable, List

class Route:
    def __init__(self, method: str, path: str, handler: Callable):
        self.method = method.upper()
        self.path = path
        self.handler = handler
        self.param_names: List[str] = []
        self.pattern = self._compile(path)

    def _compile(self, path: str) -> re.Pattern:
        parts = path.strip("/").split("/")
        regex_parts = []
        for part in parts:
            if part.startswith(":"):
                name = part[1:]
                self.param_names.append(name)
                regex_parts.append(rf"(?P<{name}>[^/]+)")
            elif part == "*":
                regex_parts.append(r"(?P<wildcard>.*)")
            else:
                regex_parts.append(re.escape(part))
        return re.compile("^/" + "/".join(regex_parts) + "/?$")

    def match(self, method: str, path: str):
        if method.upper() != self.method:
            return None
        m = self.pattern.match(path)
        return m.groupdict() if m else None


class Router:
    def __init__(self):
        self.routes: List[Route] = []

    def add_route(self, method: str, path: str, handler: Callable):
        self.routes.append(Route(method, path, handler))

    def get(self, path: str):
        def decorator(handler):
            self.add_route("GET", path, handler)
            return handler
        return decorator

    def post(self, path: str):
        def decorator(handler):
            self.add_route("POST", path, handler)
            return handler
        return decorator

    def put(self, path: str):
        def decorator(handler):
            self.add_route("PUT", path, handler)
            return handler
        return decorator

    def delete(self, path: str):
        def decorator(handler):
            self.add_route("DELETE", path, handler)
            return handler
        return decorator

    def resolve(self, method: str, path: str):
        for route in self.routes:
            params = route.match(method, path)
            if params is not None:
                return route.handler, params
        return None, None