from dotenv import load_dotenv
load_dotenv()  # optional, only if you keep a .env in prod

from app import create_app
from config import Config

app = create_app(Config)
print("DB_HOST =", app.config.get("DB_HOST"))
