import os
import yaml

from clients import Clients

CONFIGS_DIR = "config"

def load_clients(config_dir):
    clients = []
    for file_path in os.listdir(config_dir):
        if file_path.endswith(".yml"):
            client_name = file_path[:-4] + "Client"
            file_path = os.path.join(config_dir, file_path)
            with open(file_path, "r") as stream:
                client_config = yaml.load(stream)
                client = Clients[client_name](**client_config["args"])
                clients.append(client)
    return clients

def get_totals(clients):
    states = [client.get_current_state() for client in clients]
    total_current_value, total_amount_invested = map(sum, zip(*states))
    return total_current_value, total_amount_invested

def main():
    clients = load_clients(CONFIGS_DIR)

    total_current_value, total_amount_invested = get_totals(clients)

    balance = total_current_value - total_amount_invested
    roi = (balance/total_amount_invested) * 100

    print("--------------------")
    print(f"Total amount invested: ${total_amount_invested:.2f}")
    print(f"Total current value: ${total_current_value:.2f}")
    print(f"Balance: ${balance}")
    print(f"Return on investment: {roi:.2f}%")

if __name__ == "__main__":
    main()
