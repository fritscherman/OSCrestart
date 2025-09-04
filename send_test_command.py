import json
from pythonosc.udp_client import SimpleUDPClient

CONFIG_FILE = "config.json"
DEFAULT_HOST = "127.0.0.1"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def send_test_message(host: str = DEFAULT_HOST):
    cfg = load_config()
    client = SimpleUDPClient(host, cfg["port"])
    address = f"/{cfg['command']}"
    client.send_message(address, [])
    print(f"Sent {address} to {host}:{cfg['port']}")

if __name__ == "__main__":
    send_test_message()
