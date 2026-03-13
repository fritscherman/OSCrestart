import json
import sys
from pythonosc.udp_client import SimpleUDPClient

CONFIG_FILE = "config.json"
DEFAULT_HOST = "127.0.0.1"

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def send_test_message(host: str = DEFAULT_HOST, action: str = "restart"):
    cfg = load_config()
    if action == "shutdown":
        address = f"/{cfg.get('shutdown_command', 'shutdownpc')}"
    else:
        address = f"/{cfg['command']}"
    client = SimpleUDPClient(host, cfg["port"])
    client.send_message(address, [])
    print(f"Sent {address} to {host}:{cfg['port']}")

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "restart"
    send_test_message(action=action)
