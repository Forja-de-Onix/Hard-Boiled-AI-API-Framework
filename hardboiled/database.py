import os


_engine = None
_session_factory = None
_base = None
_mongo_client = None
_mongo_db = None


def _init_sql():
    global _engine, _session_factory, _base
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
    from sqlalchemy.orm import declarative_base

    engine_name = os.environ.get("DB_ENGINE", "postgres").lower()
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT")
    name = os.environ.get("DB_NAME")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")

    if engine_name == "postgres":
        port = port or "5432"
        url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"
    elif engine_name == "mysql":
        port = port or "3306"
        url = f"mysql+aiomysql://{user}:{password}@{host}:{port}/{name}"
    else:
        raise ValueError(f"DB_ENGINE SQL desconocido: '{engine_name}'")

    _engine = create_async_engine(url, echo=False)
    _session_factory = async_sessionmaker(_engine, expire_on_commit=False)
    _base = declarative_base()


def _init_mongo():
    global _mongo_client, _mongo_db
    from motor.motor_asyncio import AsyncIOMotorClient

    uri = os.environ.get("MONGO_URI")
    if not uri:
        raise ValueError("MONGO_URI no está definido en .env")

    _mongo_client = AsyncIOMotorClient(uri)
    _mongo_db = _mongo_client.get_default_database()


def init_database():
    """Resuelve y conecta la base de datos según DB_ENGINE en .env.
    Llamar una única vez al arrancar la app (p. ej. desde main.py).
    """
    engine_name = os.environ.get("DB_ENGINE", "postgres").lower()
    if engine_name in ("postgres", "mysql"):
        _init_sql()
    elif engine_name == "mongo":
        _init_mongo()
    else:
        raise ValueError(f"DB_ENGINE desconocido: '{engine_name}'")


def get_engine():
    if _engine is None:
        raise RuntimeError("Base de datos SQL no inicializada. Llama a init_database() primero.")
    return _engine


def get_session():
    if _session_factory is None:
        raise RuntimeError("Base de datos SQL no inicializada. Llama a init_database() primero.")
    return _session_factory()


def get_base():
    if _base is None:
        raise RuntimeError("Base de datos SQL no inicializada. Llama a init_database() primero.")
    return _base


def get_mongo_db():
    if _mongo_db is None:
        raise RuntimeError("Base de datos Mongo no inicializada. Llama a init_database() primero.")
    return _mongo_db