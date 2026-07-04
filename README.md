# NoteBook FanControl GUI

[Português do Brasil](README.pt-BR.md)

A small Python and GTK frontend for [nbfc-linux](https://github.com/nbfc-linux/nbfc-linux). It provides a desktop window for switching fan control modes without typing `nbfc` commands manually.

The app can:

- Enable automatic fan control.
- Set the fan to maximum speed.
- Apply a manual fan speed percentage.
- Read the current `nbfc` status when the application starts.

![Screenshot of the application](/assets/main.png "Screenshot of the application")

## Requirements

- Python 3.11 or newer.
- Poetry.
- GTK 4, libadwaita and PyGObject runtime packages for your Linux distribution.
- `nbfc-linux` installed and configured.
- `pkexec`, used when applying privileged `nbfc` changes.

This project is only a graphical frontend. Fan profiles, service setup and hardware support come from `nbfc-linux` itself.

## Install

Clone the repository:

```bash
git clone https://github.com/Andre0n/nbfc-linux-gui
cd nbfc-linux-gui
```

Install the Python dependencies:

```bash
poetry install
```

## Run

Start the application from the project directory:

```bash
poetry run python nbfc_linux_gui.py
```

You can also run the package entry point:

```bash
poetry run nbfc_linux_gui
```

When you click **Apply**, the app runs `pkexec nbfc ...`, so your desktop may ask for administrator authentication.

## Development

Useful commands:

```bash
poetry run python -m nbfc_linux_gui
poetry run blue nbfc_linux_gui tests
poetry run isort nbfc_linux_gui tests
```

The `nbfc_linux_gui.nbfc` module is a thin wrapper around the `nbfc` CLI. UI code lives under `nbfc_linux_gui/objects`.

## License

This project is licensed under LGPL-3.0. See [LICENSE](LICENSE) for details.
