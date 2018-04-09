import argparse
import time

CONFIGS_DIR = "config"

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
    web()
