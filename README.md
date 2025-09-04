# OSCrestart

A small Python tool that listens to an OSC command and restarts a running PC.
Incoming OSC messages are displayed in a debug area and also written to
`osc_restart.log`.

## Usage

Run the script and configure the OSC port, OSC command and whether the restart

should be forced using the GUI. The server starts automatically with the last
saved configuration (defaults: port `8000`, command `restartpc` and a forced
restart). Adjust values and press **Save & Restart** to apply new settings.
=======

should be forced using the GUI. The server starts automatically with the last
saved configuration (defaults: port `8000`, command `restartpc` and a forced
restart). Adjust values and press **Save & Restart** to apply new settings.
=======
should be forced using the GUI. Defaults are port `8000`, command
`restartpc` and a forced restart.


```
python osc_restart.py
```

When a message is received on the configured port with the matching OSC address
(e.g., `/restartpc`), the computer will attempt to restart. You can send a test
message from the same machine using the helper script:

```
python send_test_command.py
```

=======
=======
(e.g., `/restartpc`), the computer will attempt to restart.


