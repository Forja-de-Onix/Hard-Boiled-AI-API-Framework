import os
import time
import json
import hmac
import hashlib
import base64


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64url_decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _get_secret() -> str:
    secret = os.environ.get("JWT_SECRET")
    if not secret:
        raise RuntimeError("JWT_SECRET no está definido en .env")
    return secret


def create_token(payload: dict, expires_in: int = None) -> str:
    expires_in = expires_in or int(os.environ.get("JWT_EXPIRES_IN", "3600"))
    header = {"alg": "HS256", "typ": "JWT"}
    body = dict(payload)
    now = int(time.time())
    body["iat"] = now
    body["exp"] = now + expires_in

    segments = [
        _b64url_encode(json.dumps(header, separators=(",", ":")).encode()),
        _b64url_encode(json.dumps(body, separators=(",", ":")).encode()),
    ]
    signing_input = ".".join(segments).encode()
    signature = hmac.new(_get_secret().encode(), signing_input, hashlib.sha256).digest()
    segments.append(_b64url_encode(signature))
    return ".".join(segments)


def decode_token(token: str) -> dict:
    try:
        header_b64, body_b64, signature_b64 = token.split(".")
    except ValueError:
        raise ValueError("Token JWT malformado")

    signing_input = f"{header_b64}.{body_b64}".encode()
    expected_signature = hmac.new(_get_secret().encode(), signing_input, hashlib.sha256).digest()
    actual_signature = _b64url_decode(signature_b64)

    if not hmac.compare_digest(expected_signature, actual_signature):
        raise ValueError("Firma de token inválida")

    body = json.loads(_b64url_decode(body_b64))
    if body.get("exp", 0) < int(time.time()):
        raise ValueError("Token expirado")

    return body


def hash_password(password: str, salt: bytes = None) -> str:
    salt = salt or os.urandom(16)
    derived = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
    return f"{_b64url_encode(salt)}${_b64url_encode(derived)}"


def verify_password(password: str, stored: str) -> bool:
    try:
        salt_b64, derived_b64 = stored.split("$")
    except ValueError:
        return False
    salt = _b64url_decode(salt_b64)
    expected = _b64url_decode(derived_b64)
    actual = hashlib.scrypt(password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
    return hmac.compare_digest(expected, actual)