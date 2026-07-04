import os
import sys

from . import i18n  # noqa: F401  install gettext before any UI strings load
from gi.repository import Adw, Gdk, Gtk

from .objects.window import MainWindow

# Icons ship inside the package so the app-id icon resolves without a system
# install (dev runs, pip). Flatpak also installs them into the system theme
# for the desktop-menu entry.
_ICONS_DIR = os.path.join(os.path.dirname(__file__), 'data', 'icons')


class App(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        Gtk.IconTheme.get_for_display(
            Gdk.Display.get_default()
        ).add_search_path(_ICONS_DIR)
        self.win = MainWindow(application=app)
        self.win.present()


def main():
    app = App(application_id='io.github.andre0n.FanControl')
    app.run(sys.argv)
