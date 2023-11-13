import sys

from .app import App


def main():
    app = App(application_id='com.example.nbfc_gui')
    app.run(sys.argv)
