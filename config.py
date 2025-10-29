import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'countries.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_DIR = os.getenv("CACHE_DIR", os.path.join(BASE_DIR, "cache"))
    COUNTRIES_API_URL = os.getenv("COUNTRIES_API_URL", "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies")
    EXCHANGE_API_URL = os.getenv("EXCHANGE_API_URL", "https://open.er-api.com/v6/latest/USD")
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

