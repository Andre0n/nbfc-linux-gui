import sys

from . import i18n  # noqa: F401  install gettext before any UI strings load
from .app import App


def main():
    app = App(application_id='com.andredev.nbfc_gui')
    app.run(sys.argv)
