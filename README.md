# NoteBook FanControl GUI

This is a frontend written in Python and GTK for nbfc-linux.

Currently, the frontend allows you to configure the fan speed, providing options for both automatic control and manual adjustments based on percentage settings.

![Screenshot of the program](/assets/main.png "Screenshot of the program")

## Run Locally

Clone the project

```bash
  git clone https://github.com/Andre0n/nbfc-linux-gui
```

Go to the project directory

```bash
  cd nbfc-linux-gui
```

Install dependencies

```bash
  poetry install
```

Start the server

```bash
  poetry run python nbfc_linux_gui.py
```
