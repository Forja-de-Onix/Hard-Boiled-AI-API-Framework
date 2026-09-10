import json


class OpenAPI:
    def __init__(self, title="Hard Boiled API", version="0.1.0", description=""):
        self.title = title
        self.version = version
        self.description = description
        self.paths = {}

    def add_route(self, method, path, summary=None, description=None,
                  request_body=None, responses=None, tags=None, security=None):
        openapi_path = self._to_openapi_path(path)
        entry = self.paths.setdefault(openapi_path, {})
        operation = {
            "summary": summary or "",
            "description": description or "",
            "tags": tags or [],
        }
        if request_body:
            operation["requestBody"] = {"content": {"application/json": {"schema": request_body}}}
        operation["responses"] = responses or {"200": {"description": "OK"}}
        if security:
            operation["security"] = security
        entry[method.lower()] = operation

    @staticmethod
    def _to_openapi_path(path: str) -> str:
        # /users/:id -> /users/{id}  (OpenAPI usa llaves, no dos puntos)
        parts = path.strip("/").split("/")
        converted = [f"{{{p[1:]}}}" if p.startswith(":") else p for p in parts]
        return "/" + "/".join(converted)

    def to_spec(self) -> dict:
        return {
            "openapi": "3.0.3",
            "info": {"title": self.title, "version": self.version, "description": self.description},
            "paths": self.paths,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_spec())