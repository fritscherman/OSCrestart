# OSCrestart

A small Python tool that listens to OSC commands and restarts or shuts down a
running PC. Incoming OSC messages are displayed in a debug area and also written
to `osc_restart.log`.

## Usage

Run the script and configure the OSC port, restart command, shutdown command and
whether the action should be forced using the GUI. The server starts
automatically with the last saved configuration (defaults: port `8000`, restart
command `restartpc`, shutdown command `shutdownpc` and a forced action). Adjust
values and press **Save & Restart** to apply new settings.

```
python osc_restart.py
```

When a message is received on the configured port with the matching OSC address
(e.g., `/restartpc`), the computer will attempt to restart. When the shutdown
address is received (e.g., `/shutdownpc`), the computer will shut down instead.
You can send a test message from the same machine using the helper script:

```
python send_test_command.py            # sends a restart command
python send_test_command.py shutdown   # sends a shutdown command
```
