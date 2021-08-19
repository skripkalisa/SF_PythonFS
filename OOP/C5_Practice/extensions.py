import requests
import json
from config import keys, help_text

class ConvertException(Exception):
    pass

class CurrencyConvertor:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base: 
            raise ConvertException(f'Вы пытаетесь перевести {base} в {quote} \
                {help_text}')

        try: 
            amount = float(amount)
        except ValueError:
            raise ConvertException(f'Не могу обработать число: {amount} \
                {help_text}')

        try: 
            base_cur = keys[base]
        except KeyError:
            raise ConvertException(f'Не могу обработать валюту: {base} \
                {help_text}')

        try: 
            quote_cur = keys[quote]
        except KeyError:
            raise ConvertException(f'Не могу обработать валюту: {quote} \
                {help_text}')

        url = f'https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/{base_cur}/{quote_cur}.json'

        r = requests.get(url)
        get_quote = json.loads(r.content)[keys[quote]]
        return get_quote
