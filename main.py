import argparse

from cryptobalance import CryptoBalance

CONFIGS_DIR = "config"

def cli():
    crypto_balance = CryptoBalance(CONFIGS_DIR)
    crypto_balance.update()
    if len(crypto_balance.clients) > 0:
        print(crypto_balance.state())
    else:
        print("No clients were setup. Exiting.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CLI tool that collects your portfolio data from GDAX/Coinbase.')
    parser.add_argument('--web-ui', action="store_true", default=False)
    args = parser.parse_args()
    web_ui = args.web_ui

    if not web_ui:
        cli()
    else:
        from web_ui import app
        app.app.run(host="0.0.0.0", port=8000)
