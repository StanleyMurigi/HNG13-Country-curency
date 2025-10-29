import requests
from config import Config
from utils.errors import external_unavailable

def fetch_countries():
    try:
        resp = requests.get(Config.COUNTRIES_API_URL, timeout=Config.REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        # caller will handle error format
        return None

def fetch_exchange_rates():
    try:
        resp = requests.get(Config.EXCHANGE_API_URL, timeout=Config.REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        # expected structure: { "result": "success", "rates": { "NGN": 1600.23, ... } }
        rates = data.get("rates")
        return rates
    except Exception as e:
        return None

