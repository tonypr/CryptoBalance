import os
import yaml
import datetime

from cryptobalance.CryptoClient import CryptoClient
from cryptobalance.clients import Clients

CONFIGS_DIR = "config"

def load_clients(config_dir):
    clients = []
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)

    for client in Clients:
        file_path = os.path.join(config_dir, client) + ".yml"
        if os.path.isfile(file_path):
            with open(file_path, "r") as stream:
                client_config = yaml.load(stream)
                if "TODO" in client_config["args"].values():
                    print(f"Configuration for {client} is not set. Please enter the correct configuration in {file_path}.")
                    continue
                client = Clients[client](**client_config["args"])
                clients.append(client)
        else:
            with open(file_path, "w") as f:
                client_class = Clients[client]
                data = CryptoClient.setup_config(client_class)
                yaml.dump(data, f, default_flow_style=False)
                print(f"Generating {file_path} for {client} configuration.")
    return clients

class CryptoBalance(object):
    def __init__(self, config_dir):
        self.clients = load_clients(config_dir)
        self.total_current_value = 0
        self.total_amount_invested = 0
        self.balance = 0
        self.roi = 0
        self.product_values = {}

    def update(self):
        if len(self.clients) == 0:
            print("*WARNING*: No clients were loaded. Could not update.")

        states = [client.get_current_state() for client in self.clients]
        product_values = {}
        for client in self.clients:
            client_values = client.get_product_values()
            for product, value in client_values.items():
                if product not in product_values:
                    product_values[product] = 0
                else:
                    product_values[product] += round(value, 2)
        chart_settings = {
            "labels": [],
            "data": [],
        }
        for product, value in product_values.items():
            chart_settings["labels"].append(product)
            chart_settings["data"].append(value)
        self.product_values = chart_settings
        self.total_current_value, self.total_amount_invested = map(sum, zip(*states))
        self.balance = self.total_current_value - self.total_amount_invested
        self.roi = (self.balance/self.total_amount_invested) * 100

    def state(self):
        if self.balance >= 0:
            balance_str = f"${self.balance:.2f}"
        else:
            balance_str = f"-${-self.balance:.2f}"

        return {
            "total_amount_invested": f"${self.total_amount_invested:.2f}",
            "total_current_value": f"${self.total_current_value:.2f}",
            "balance": balance_str,
            "roi": f"{self.roi:.2f}%",
            "product_values": self.product_values,
        }

def main():
    crypto_balance = CryptoBalance(CONFIGS_DIR)
    crypto_balance.update()
    if len(crypto_balance.clients) > 0:
        print(crypto_balance.state())
    else:
        print("No clients were setup. Exiting.")

if __name__ == "__main__":
    main()
