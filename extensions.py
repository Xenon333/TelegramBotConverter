import requests
import json
from config import keys
from config import headers

class ConvertionException(Exception):
    pass

class CurrencyConverter(Exception):
    @staticmethod
    def get_price(base: str, quote: str, amount):
        if quote == base:
            raise ConvertionException(f"Невозможно перевести одинаковые валюты {base}.")

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {base}")

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f"Не удалось обработать валюту {quote}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Не удалось обработать количество {amount}")

        r = requests.get(f"https://api.apilayer.com/fixer/convert?to={quote_ticker}&from={base_ticker}&amount={amount}", headers=headers)
        total = json.loads(r.content)

        return total
