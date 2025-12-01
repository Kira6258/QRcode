import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'instance'))
os.makedirs(BASE_DIR, exist_ok=True)

class Config:
    SECRET_KEY = "secret123"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "history.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
