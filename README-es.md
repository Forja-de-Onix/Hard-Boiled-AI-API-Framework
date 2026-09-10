# Hard Boiled AI API Framework

Un **framework** asíncrono y ligero para construir APIs nativas de IA en Python — inspirado en la ergonomía de Express.js, con un núcleo sin dependencias: enrutamiento, middlewares, autenticación JWT y documentación OpenAPI/Swagger corren sobre `asyncio` puro y la librería estándar. Por encima: acceso a datos SQL/NoSQL opcional y conectores multi-proveedor de IA (Ollama, Claude, Gemini, ChatGPT) con soporte de streaming.

> 🇬🇧 English version: [README.md](README.md)

## ¿Por qué Hard Boiled?

La mayoría de frameworks en Python o bien imponen un ORM y stack de plantillas específico (Django), o dejan todo en manos de paquetes de terceros sin estructura de opinión (Flask puro). Hard Boiled queda en un punto intermedio: un núcleo `asyncio` puro **sin dependencias obligatorias** — ni siquiera para JWT o documentación de API — más un scaffold oficial y un conjunto curado de integraciones de primera parte que configuras íntegramente por `.env`, sin tocar código del framework.

## Funcionalidades

- Servidor HTTP en `asyncio` puro como núcleo — sin dependencias para arrancar
- Enrutamiento estilo Express: `app.get("/users/:id")`, parámetros dinámicos, wildcards
- Pipeline de middlewares, global (`app.use`) o por ruta
- Objeto `Response` inspirado en `httpx`, con streaming por chunks nativo
- Autenticación JWT y hashing de contraseñas con `scrypt` — solo librería estándar
- Documentación Swagger/OpenAPI en `/docs`, generada sin dependencias externas
- Scaffold de proyecto oficial: `controllers/`, `routes/`, `models/`, `middlewares/` en la capa de la app, separados del núcleo `hardboiled/`
- Configuración por `.env`: motor de base de datos (Postgres, MySQL, MongoDB) y conector de IA (Ollama, Claude, Gemini, ChatGPT)
- Listo para pytest, con un workflow mínimo de GitHub Actions para CI

## Instalación

```bash
git clone <url-de-tu-repo>
cd hard-boiled-ai-api-framework
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

Y para los conectores de IA (todos, incluido Ollama, llaman a una API HTTP):

```bash
pip install httpx
```

Luego edita `.env` y ejecuta:

```bash
python main.py
```

## Inicio rápido

Consulta el [Inicio Rápido](wiki/es/06.Inicio-Rapido.md) completo para enrutamiento, middlewares, base de datos, IA, autenticación JWT y documentación Swagger de principio a fin. Ejemplo mínimo:

```python
from hardboiled import App

app = App()

@app.get("/")
async def index(req, res):
    res.json({"message": "Hard Boiled funcionando"})

app.listen(3000)
```

## Testing

```bash
pip install -r requirements-dev.txt
pytest
```

Un workflow mínimo de GitHub Actions (`.github/workflows/tests.yml`) ejecuta esto en cada push y pull request. Ver [Testing y CI](wiki/es/11.Testing-CI.md).

## Documentación

La documentación completa está en la [wiki](wiki/es/01.Home.md). Empieza por [Setup](wiki/es/02.Setup.md) para configurar tu `.env` antes que nada.

## Estado

En desarrollo temprano — la API todavía no es estable.

## Licencia

Este proyecto está licenciado bajo la **GNU General Public License v3.0 (GPLv3)** — consulta el archivo [LICENSE](LICENSE) para el texto completo.