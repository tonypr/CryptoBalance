import argparse
import time

CONFIGS_DIR = "config"

def cli():
    from cryptobalance import CryptoBalance
    crypto_balance = CryptoBalance(CONFIGS_DIR)
    crypto_balance.update()
    if len(crypto_balance.clients) > 0:
        print(crypto_balance.state())
    else:
        print("No clients were setup. Exiting.")

def web():
    try:
        import subprocess
        proc1 = subprocess.Popen(["python3","-m","web_ui.app_microservice"])
        time.sleep(7)
        from web_ui.app_main import app
        app.run(host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        if proc1:
            proc1.kill()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='CLI tool that collects your portfolio data from GDAX/Coinbase.')
    parser.add_argument('--web-ui', action="store_true", default=False)
    args = parser.parse_args()

    proc1 = None
    if args.web_ui:
        web()
    else:
        cli()
