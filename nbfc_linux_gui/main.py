import sys

from . import i18n  # noqa: F401  install gettext before any UI strings load
from gi.repository import Adw

from .objects.window import MainWindow


class App(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()


def main():
    app = App(application_id='com.andredev.nbfc_gui')
    app.run(sys.argv)
