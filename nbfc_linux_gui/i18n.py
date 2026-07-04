"""gettext setup. Import `_` from here to mark translatable strings."""
import gettext
import os

DOMAIN = 'nbfc_gui'
LOCALE_DIR = os.path.join(os.path.dirname(__file__), 'locale')

gettext.bindtextdomain(DOMAIN, LOCALE_DIR)
gettext.textdomain(DOMAIN)

_translation = gettext.translation(DOMAIN, LOCALE_DIR, fallback=True)
_ = _translation.gettext
