# Hard Boiled AI API Framework

Un **framework** asíncrono y ligero para construir APIs nativas de IA en Python — inspirado en la ergonomía de Express.js, con un núcleo sin dependencias obligatorias y extensiones oficiales opcionales para desarrollo REST tradicional: acceso a datos SQL/NoSQL, autenticación JWT, documentación Swagger, y conectores multi-proveedor de IA (Ollama, Claude, Gemini, ChatGPT) con soporte de streaming.

> 🇬🇧 English version: [README.md](README.md)

## ¿Por qué Hard Boiled?

La mayoría de frameworks en Python o bien imponen un ORM y stack de plantillas específico (Django), o dejan todo en manos de paquetes de terceros sin estructura de opinión (Flask puro). Hard Boiled queda en un punto intermedio: un núcleo `asyncio` puro **sin dependencias obligatorias**, más un scaffold oficial y un conjunto curado de integraciones de primera parte que configuras íntegramente por `.env` — motor de base de datos, proveedor de IA y comportamiento de streaming — sin tocar código del framework.

## Funcionalidades (actuales)

- Servidor HTTP en `asyncio` puro como núcleo — sin dependencias para arrancar
- Enrutamiento estilo Express: `app.get("/users/:id")`, parámetros dinámicos, wildcards
- Pipeline de middlewares con `app.use(...)` y `next()`
- Objeto `Response` inspirado en `httpx` (`.json()`, `.text()`, `.status()`), con streaming por chunks nativo
- Scaffold de proyecto oficial: `controllers/`, `routes/`, `models/`, `middlewares/` en la capa de la app, separados del núcleo `hardboiled/` (que contiene `app.py`, `router.py`, `connectors.py`, `database.py`)
- Configuración por `.env`: elige tu motor de base de datos (Postgres, MySQL, MongoDB) y tu conector de IA (Ollama, Claude, Gemini, ChatGPT) sin tocar código

## Hoja de ruta

- `hardboiled/database.py`: resolver SQLAlchemy vs Mongoengine/Motor según `DB_ENGINE`
- `hardboiled/connectors.py`: interfaz unificada entre Ollama/Claude/Gemini/ChatGPT con streaming
- Middleware de autenticación JWT
- Generación de documentación Swagger/OpenAPI
- Contenedores Docker para el framework y sus integraciones oficiales
- `requirements.txt` con extras de instalación a medida que se añaden dependencias

## Instalación

```bash
git clone <url-de-tu-repo>
cd hard-boiled-ai-api-microframework
cp .env.example .env
```

El núcleo no tiene dependencias obligatorias. Instala solo lo que necesite tu `DB_ENGINE` elegido:

```bash
# Postgres
pip install sqlalchemy[asyncio] asyncpg

# MySQL
pip install sqlalchemy[asyncio] aiomysql

# MongoDB
pip install motor
```

Y para los conectores de IA que llaman a una API HTTP (todos, incluido Ollama):

```bash
pip install httpx
```

Luego edita `.env` — consulta [Setup](wiki/es/Setup.md) para más detalle — y ejecuta:

```bash
python main.py
```

## Inicio rápido

```bash
python main.py
```

```python
from hardboiled import App

app = App()

@app.get("/")
async def index(req, res):
    res.json({"message": "Hard Boiled funcionando"})

app.listen(3000)
```

## Documentación

La documentación completa está en la [wiki](wiki/es/Home.md). Empieza por [Setup](wiki/es/Setup.md) para configurar tu `.env` antes que nada.

## Estado

En desarrollo temprano — la API todavía no es estable.

## Licencia

Por definir