from gi.repository import Adw, Gtk

from ..i18n import _


class ModeSelector(Gtk.Box):
    """Native segmented pill (Adw.ToggleGroup): auto / max / custom.

    Adw.ToggleGroup is a final type, so we wrap it rather than subclass.
    Calls on_change(mode) whenever the active mode changes.
    """

    MODES = ('auto', 'max', 'custom')

    def __init__(self, on_change=None):
        super().__init__()
        self._on_change = on_change

        self._group = Adw.ToggleGroup()
        self._group.add_css_class('mode-selector')
        self._group.set_homogeneous(True)
        self._group.set_hexpand(True)
        self.append(self._group)

        labels = {'auto': _('Automatic'), 'max': _('Maximum'), 'custom': _('Manual')}
        for mode in self.MODES:
            self._group.add(Adw.Toggle(name=mode, label=labels[mode]))

        self._group.connect('notify::active', self._changed)

    def _changed(self, *_args):
        if self._on_change:
            self._on_change(self.get_mode())

    def get_mode(self):
        return self._group.get_active_name() or self.MODES[0]

    def set_mode(self, mode):
        self._group.set_active_name(mode)
