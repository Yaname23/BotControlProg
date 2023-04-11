import json
import requests
from config import keys

class ConvertionException(Exception):#исключение
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты (" {base} " в " {base} " ).')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Вы допустили ошибку в названии валюты "{quote}"')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Вы допустили ошибку в названии валюты "{base}"')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'не удалось обработать указанное количество ({amount})')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
