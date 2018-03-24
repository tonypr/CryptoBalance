from CryptoClient import CryptoClient

import gdax

class GdaxClient(CryptoClient):
    def __init__(self, key, b64secret, passphrase):
        self.client = gdax.AuthenticatedClient(key, b64secret, passphrase)
        self.accounts = self.client.get_accounts()

    def get_product_ids_usd(self):
        USD_SUFFIX = "-USD"
        product_list = self.client.get_products()
        product_ids = [elem['id'] for elem in product_list]
        product_ids_usd = [elem for elem in product_ids if USD_SUFFIX in elem]
        return product_ids_usd

    def get_product_prices(self):
        ids = self.get_product_ids_usd()
        product_prices = {}
        for product_id in ids:
            value = self.client.get_product_ticker(product_id=product_id)["price"]
            product_prices[product_id[:3]] = float(value)
        return product_prices

    def get_product_values(self):
        prices = self.get_product_prices()
        values = {}
        for account in self.accounts:
            currency = account["currency"]
            amount = float(account["available"]) + float(account["hold"])
            if currency in prices:
                values[currency] = amount*prices[currency]
            else:
                values[currency] = amount
        return values

    def get_current_value(self):
        values = self.get_product_values()
        total = sum(v for k,v in values.items())
        return total

    def get_amount_invested(self):
        return 0
