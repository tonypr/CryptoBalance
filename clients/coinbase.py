from CryptoClient import CryptoClient

from coinbase.wallet.client import Client

PRIMARY_ACCOUNT_CURRENCY = "USD"

class CoinbaseClient(CryptoClient):
    def __init__(self, key, secret):
        self.client = Client(key, secret)
        self.accounts = self.client.get_accounts()["data"]
        for account in self.accounts:
            if account["balance"]["currency"] == PRIMARY_ACCOUNT_CURRENCY:
                self.account = account
                break

    def get_current_value(self):
        values = {}
        for account in self.accounts:
            currency = account["balance"]["currency"]
            values[currency] = float(account["native_balance"]["amount"])
        return sum(v for k,v in values.items())

    def get_account_total(self, account):
        transactions = account.get_transactions()["data"]
        total = 0
        for transaction in transactions:
            transaction_type = transaction["type"]
            if transaction_type in ["exchange_deposit", "exchange_withdrawl"]:
                continue
            total += float(transaction["native_amount"]["amount"])
        return total

    def get_amount_invested(self):
        return sum(self.get_account_total(account) for account in self.accounts)
