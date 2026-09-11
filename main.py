from hardboiled import App
from hardboiled.config import load_env
from hardboiled.ai_response import ask
from hardboiled.database import init_database

load_env()

app = App()

if __name__ == "__main__":
    app.listen(3000)