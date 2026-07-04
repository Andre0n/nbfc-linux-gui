import gi

# Pin toolkit versions before any gi.repository import anywhere in the package.
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
