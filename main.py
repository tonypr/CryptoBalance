import os
import yaml

from CryptoClient import CryptoClient
from clients import Clients

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

def get_totals(clients):
    states = [client.get_current_state() for client in clients]
    total_current_value, total_amount_invested = map(sum, zip(*states))
    return total_current_value, total_amount_invested

def main():
    clients = load_clients(CONFIGS_DIR)
    if len(clients) > 0:
        total_current_value, total_amount_invested = get_totals(clients)
        balance = total_current_value - total_amount_invested
        roi = (balance/total_amount_invested) * 100

        print("--------------------")
        print(f"Total amount invested: ${total_amount_invested:.2f}")
        print(f"Total current value: ${total_current_value:.2f}")
        print(f"Balance: ${balance}")
        print(f"Return on investment: {roi:.2f}%")
    else:
        print("No clients were setup. Exiting.")

if __name__ == "__main__":
    main()
