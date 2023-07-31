import requests
import json
from key_s import keys

class APIException(Exception):
    pass


class ExchangeConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: int):
        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты {base}.')

        try:
           base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}.')

        try:
           quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}.')

        try:
           amount = int(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}.')
        if amount <= 0:
            raise APIException(f'Невозможно конвертировать количество валюты {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = json.loads(r.content)[keys[quote]]

        return total_base*amount
