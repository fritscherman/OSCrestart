import json
import logging
import os
import platform
import threading
from queue import Queue
from tkinter import Tk, Label, Entry, Button, Checkbutton, BooleanVar, Text, END

try:
    from pythonosc.dispatcher import Dispatcher
    from pythonosc.osc_server import ThreadingOSCUDPServer
except ImportError:
    Dispatcher = None
    ThreadingOSCUDPServer = None

CONFIG_FILE = "config.json"
LOG_FILE = "osc_restart.log"
DEFAULT_PORT = 8000
DEFAULT_COMMAND = "restartpc"
DEFAULT_FORCE = True

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)


def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "port": DEFAULT_PORT,
            "command": DEFAULT_COMMAND,
            "force": DEFAULT_FORCE,
        }


def save_config(port, command, force):
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump({"port": port, "command": command, "force": force}, file)


def restart_system(force):  # pragma: no cover - system call
    system = platform.system()
    if system == "Windows":
        cmd = "shutdown /r /t 0"
        if force:
            cmd = "shutdown /r /f /t 0"
    else:
        cmd = "sudo shutdown -r now"
        if force:
            cmd = "sudo shutdown -r -f now"
    os.system(cmd)


def start_server(port, command, force, log_queue):
    if Dispatcher is None or ThreadingOSCUDPServer is None:
        raise ImportError("python-osc is required to run the OSC server")

    dispatcher = Dispatcher()

    def handle(address, *args):
        msg = f"Received {address} {' '.join(map(str, args))}".strip()
        logging.info(msg)
        log_queue.put(msg)
        if address == f"/{command}":
            restart_system(force)

    dispatcher.set_default_handler(handle)
    server = ThreadingOSCUDPServer(("0.0.0.0", port), dispatcher)
    logging.info("Listening on port %s for /%s", port, command)
    server.serve_forever()


def build_gui():
    cfg = load_config()

    root = Tk()
    root.title("OSC Restart Config")

    Label(root, text="OSC Restart Listener").grid(row=0, column=0, columnspan=2)
    Label(root, text="Port:").grid(row=1, column=0)
    port_entry = Entry(root)
    port_entry.insert(0, str(cfg["port"]))
    port_entry.grid(row=1, column=1)

    Label(root, text="Command:").grid(row=2, column=0)
    cmd_entry = Entry(root)
    cmd_entry.insert(0, cfg["command"])
    cmd_entry.grid(row=2, column=1)

    force_var = BooleanVar(value=cfg.get("force", DEFAULT_FORCE))
    Checkbutton(root, text="Force restart", variable=force_var).grid(
        row=3, column=0, columnspan=2
    )

    log_text = Text(root, height=8, width=40, state="disabled")
    log_text.grid(row=5, column=0, columnspan=2)
    Label(root, text="Configure and start. Incoming commands appear below.").grid(
        row=4, column=0, columnspan=2
    )

    log_queue = Queue()

    def poll_log():
        while not log_queue.empty():
            message = log_queue.get()
            log_text.configure(state="normal")
            log_text.insert(END, message + "\n")
            log_text.configure(state="disabled")
            log_text.see(END)
        root.after(100, poll_log)

    def save_and_start():
        port = int(port_entry.get())
        cmd = cmd_entry.get()
        force = force_var.get()
        save_config(port, cmd, force)
        threading.Thread(
            target=start_server, args=(port, cmd, force, log_queue), daemon=True
        ).start()

    Button(root, text="Save & Start", command=save_and_start).grid(
        row=6, column=0, columnspan=2
    )

    poll_log()
    root.mainloop()


if __name__ == "__main__":
    build_gui()
