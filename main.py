from hardboiled import App
from hardboiled.config import load_env
from hardboiled.ai_response import ask
from hardboiled.database import init_database


load_env()
init_database()

app = App()


async def logger_middleware(req, res, next):
    print(f"{req.method} {req.path}")
    await next()


app.use(logger_middleware)


@app.get("/")
async def index(req, res):
    res.json({"message": "Hard Boiled AI API Framework funcionando"})


@app.post("/ask")
async def ask_endpoint(req, res):
    body = req.json()
    prompt = body.get("prompt")

    if not prompt:
        res.status(400).json({"error": "El campo 'prompt' es obligatorio"})
        return

    result = await ask(
        prompt,
        model=body.get("model"),
        stream=body.get("stream"),
    )

    if hasattr(result, "__aiter__"):
        res.stream(result)
    else:
        res.json({"response": result})


if __name__ == "__main__":
    app.listen(3000)