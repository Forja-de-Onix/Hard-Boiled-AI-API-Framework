from hardboiled.auth import decode_token


async def jwt_auth_middleware(req, res, next):
    """Middleware para proteger rutas concretas con JWT.
    Se aplica por ruta (no con app.use), para no bloquear /login."""
    auth_header = req.headers.get("authorization", "")
    if not auth_header.startswith("Bearer "):
        res.status(401).json({"error": "Falta el token Bearer"})
        return

    token = auth_header[len("Bearer "):]
    try:
        req.user = decode_token(token)
    except ValueError as exc:
        res.status(401).json({"error": str(exc)})
        return

    await next()