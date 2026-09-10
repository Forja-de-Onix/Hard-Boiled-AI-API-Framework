# Hard Boiled AI API Framework

A lightweight async **framework** for building AI-native APIs in Python — inspired by Express.js's ergonomics, with a dependency-free core: routing, middleware, JWT auth, and OpenAPI/Swagger docs all run on pure `asyncio` and the standard library. On top: opt-in SQL/NoSQL data access and multi-provider AI connectors (Ollama, Claude, Gemini, ChatGPT) with streaming support.

> 🇪🇸 Looking for Spanish? See [README-es.md](README-es.md)

## Why Hard Boiled?

Most Python frameworks either force a specific ORM and templating stack (Django) or leave everything to third-party packages with no opinionated structure (raw Flask). Hard Boiled sits in between: a pure `asyncio` core with **no required dependencies** — not even for JWT auth or API docs — plus an official scaffold and a curated set of first-party integrations you configure entirely through `.env`, without touching framework code.

## Features

- Pure `asyncio` HTTP server at the core — no dependencies required to run
- Express-style routing: `app.get("/users/:id")`, dynamic params, wildcards
- Middleware pipeline, global (`app.use`) or per-route
- `httpx`-inspired `Response` object with native chunked streaming
- JWT authentication and `scrypt` password hashing — stdlib only
- Swagger/OpenAPI docs at `/docs`, generated without external dependencies
- Official project scaffold: `controllers/`, `routes/`, `models/`, `middlewares/` at the app layer, separate from the `hardboiled/` core
- Configuration-driven setup via `.env`: database engine (Postgres, MySQL, MongoDB) and AI connector (Ollama, Claude, Gemini, ChatGPT)
- pytest-ready, with a minimal GitHub Actions workflow for CI

## Installation

```bash
git clone <your-repo-url>
cd hard-boiled-ai-api-framework
cp .env.example .env
```

The core has no required dependencies. Install only what your chosen `DB_ENGINE` needs:

```bash
# Postgres
pip install sqlalchemy[asyncio] asyncpg

# MySQL
pip install sqlalchemy[asyncio] aiomysql

# MongoDB
pip install motor
```

And for AI connectors (all of them, including Ollama, call an HTTP API):

```bash
pip install httpx
```

Then edit `.env` and run:

```bash
python main.py
```

## Quick start

See the full [Quick Start](wiki/en/06.Quick-Start.md) for routing, middleware, database, AI, JWT auth, and Swagger docs end to end. Minimal example:

```python
from hardboiled import App

app = App()

@app.get("/")
async def index(req, res):
    res.json({"message": "Hard Boiled is running"})

app.listen(3000)
```

## Testing

```bash
pip install -r requirements-dev.txt
pytest
```

A minimal GitHub Actions workflow (`.github/workflows/tests.yml`) runs this on every push and pull request. See [Testing & CI](wiki/en/11.Testing-CI.md).

## Documentation

Full docs live in the [wiki](wiki/en/01.Home.md). Start with [Setup](wiki/en/02.Setup.md) to configure your `.env` before anything else.

## Status

Early development — API surface is not stable yet.

## License

This project is licensed under the **GNU General Public License v3.0 (GPLv3)** — see the [LICENSE](LICENSE) file for the full text.

In short: you're free to use, modify, and redistribute this project, including commercially, as long as any distributed derivative work is also licensed under GPLv3 and its source code remains available. This is a copyleft license — it doesn't restrict how you use Tanuki to build your own projects, but if you modify and redistribute Tanuki itself, those modifications must stay open under the same terms.