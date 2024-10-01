import requests
import environ
import os
from pathlib import Path

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

API_KEY = env('EXCHANGE_API_KEY')
BASE_URL = 'https://v6.exchangerate-api.com/v6/'
def get_exchange_rates(base_currency='USD'):
    url = f"{BASE_URL}{API_KEY}/latest/{base_currency}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception("Error fetching exchange rates")