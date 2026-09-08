# Hard Boiled AI API Framework

A lightweight async **framework** for building AI-native APIs in Python — inspired by Express.js's ergonomics, with a dependency-free core and official, opt-in extensions for GraphQL-free REST development: SQL/NoSQL data access, JWT auth, Swagger docs, and multi-provider AI connectors (Ollama, Claude, Gemini, ChatGPT) with streaming support.

> 🇪🇸 Looking for Spanish? See [README-es.md](README-es.md)

## Why Hard Boiled?

Most Python frameworks either force a specific ORM and templating stack (Django) or leave everything to third-party packages with no opinionated structure (raw Flask). Hard Boiled sits in between: a pure `asyncio` core with **no required dependencies**, plus an official scaffold and a curated set of first-party integrations you configure entirely through `.env` — database engine, AI provider, and streaming behavior — without touching framework code.

## Features (current)

- Pure `asyncio` HTTP server at the core — no dependencies required to run
- Express-style routing: `app.get("/users/:id")`, dynamic params, wildcards
- Middleware pipeline with `app.use(...)` and `next()`
- `httpx`-inspired `Response` object (`.json()`, `.text()`, `.status()`), with native chunked streaming
- Official project scaffold: `controllers/`, `routes/`, `models/`, `middlewares/` at the app layer, separate from the `hardboiled/` core (which holds `app.py`, `router.py`, `connectors.py`, `database.py`)
- Configuration-driven setup via `.env`: choose your database engine (Postgres, MySQL, MongoDB) and your AI connector (Ollama, Claude, Gemini, ChatGPT) without editing code

## Roadmap

- `hardboiled/database.py`: resolve SQLAlchemy vs Mongoengine/Motor based on `DB_ENGINE`
- `hardboiled/connectors.py`: unified interface across Ollama/Claude/Gemini/ChatGPT with streaming
- JWT authentication middleware
- Swagger/OpenAPI documentation generation
- Docker containers for the framework and its official integrations
- `requirements.txt` with install extras as dependencies are added

## Quick start

```bash
python main.py
```

```python
from hardboiled import App

app = App()

@app.get("/")
async def index(req, res):
    res.json({"message": "Hard Boiled is running"})

app.listen(3000)
```

## Documentation

Full docs live in the [wiki](wiki/en/Home.md). Start with [Setup](wiki/en/Setup.md) to configure your `.env` before anything else.

## Status

Early development — API surface is not stable yet.

## License

TBD