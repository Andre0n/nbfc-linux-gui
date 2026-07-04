from gi.repository import Adw, Gdk, Gio, Gtk

from .. import nbfc
from ..i18n import _
from .fan_widget import FanWidget
from .mode_selector import ModeSelector

MAIN_BOX_PADDING = 18
MAIN_BOX_SPACING = 14

# Mode -> subtitle shown under the fan.
_MODE_SUBTITLE = {
    'auto': _('Automatic adjustment'),
    'max': _('Maximum speed'),
    'custom': _('Manual adjustment'),
}

CSS = """
@define-color accent_bg_color #3584e4;
@define-color accent_color #3584e4;
@define-color accent_fg_color #ffffff;
.apply-btn { padding-top: 8px; padding-bottom: 8px; font-weight: bold; }
.mode-selector { border-radius: 8px; background: alpha(@window_fg_color, 0.08); }
.mode-selector toggle { padding: 3px 4px; }
.mode-selector toggle:checked { background: @accent_bg_color; color: @accent_fg_color; }
"""


class MainWindow(Adw.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(360, 480)
        self.set_resizable(False)
        self.set_title(_('Fan Control'))

        self._install_css()

        self.main_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=MAIN_BOX_SPACING,
            margin_top=MAIN_BOX_PADDING,
            margin_bottom=MAIN_BOX_PADDING,
            margin_start=MAIN_BOX_PADDING,
            margin_end=MAIN_BOX_PADDING,
        )

        toolbar = Adw.ToolbarView()
        header = Adw.HeaderBar()
        header.add_css_class('flat')
        header.pack_start(self._build_menu_button())
        toolbar.add_top_bar(header)
        toolbar.set_content(self.main_box)
        self.set_content(toolbar)

        self._build_fan()

        self.modes = ModeSelector(on_change=self._mode_changed)
        self.modes.set_halign(Gtk.Align.FILL)
        self.modes.set_hexpand(True)
        self.main_box.append(self.modes)

        self._build_slider()

        self.apply_button = Gtk.Button(
            label=_('Apply'),
            css_classes=['suggested-action', 'apply-btn'],
            hexpand=True,
        )
        self.apply_button.connect('clicked', self._apply)
        self.main_box.append(self.apply_button)

        self.modes.set_mode('auto')
        self._mode_changed('auto')
        self.load_current_status()

    def _build_menu_button(self):
        """Hamburger menu (top-left) with an About entry."""
        action = Gio.SimpleAction.new('about', None)
        action.connect('activate', self._show_about)
        self.add_action(action)

        menu = Gio.Menu()
        menu.append(_('About'), 'win.about')

        return Gtk.MenuButton(
            icon_name='open-menu-symbolic',
            menu_model=menu,
            tooltip_text=_('Main Menu'),
        )

    def _show_about(self, _action, _param):
        about = Adw.AboutDialog(
            application_name=_('Fan Control'),
            application_icon='com.andredev.nbfc_gui',
            developer_name='André Gabriel',
            version='0.1.0',
            comments=_('A frontend to nbfc-linux.'),
            website='https://github.com/Andre0n/nbfc-linux-gui',
            issue_url='https://github.com/Andre0n/nbfc-linux-gui/issues',
            license_type=Gtk.License.LGPL_3_0,
            copyright='© 2026 André Gabriel',
        )
        about.present(self)

    @staticmethod
    def _install_css():
        """Load app CSS once for the whole display, not per widget."""
        provider = Gtk.CssProvider()
        provider.load_from_data(CSS.encode())
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def _build_fan(self):
        self.fan = FanWidget()
        self.fan.set_halign(Gtk.Align.CENTER)
        self.main_box.append(self.fan)

        # Subtitle under the fan: active mode / status / errors.
        self.status_label = Gtk.Label(
            css_classes=['dim-label', 'caption'],
            halign=Gtk.Align.CENTER,
        )
        self.main_box.append(self.status_label)

    def _build_slider(self):
        row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        row.append(Gtk.Label(label=_('Speed'), halign=Gtk.Align.START))
        self.percent_label = Gtk.Label(
            halign=Gtk.Align.END, hexpand=True,
            css_classes=['numeric'],
        )
        row.append(self.percent_label)
        self.main_box.append(row)

        self.slider = Gtk.Scale()
        self.slider.set_digits(0)
        self.slider.set_range(10, 100)
        self.slider.set_draw_value(False)
        self.slider.set_value(50)
        self.slider.connect('value-changed', self._slider_changed)
        self.main_box.append(self.slider)

    def _slider_changed(self, scale):
        value = scale.get_value()
        self.fan.set_speed(value)
        self.percent_label.set_label(f'{value:.0f}%')

    def _mode_changed(self, mode):
        """One mode active at a time. Slider only matters in Custom."""
        self.slider.set_sensitive(mode == 'custom')
        self.status_label.set_label(_MODE_SUBTITLE.get(mode, ''))
        if mode == 'max':
            speed = 100
        elif mode == 'auto':
            speed = 50            # auto: moderate preview spin
        else:
            speed = self.slider.get_value()
        self.fan.set_speed(speed)
        self.percent_label.set_label(f'{speed:.0f}%')

    def load_current_status(self):
        """Read current fan config from nbfc and reflect it in the UI."""
        status = nbfc.status()
        if status is None:
            return  # nbfc unavailable: keep defaults

        auto = status.get('Auto Control Enabled', '').lower() == 'true'
        self.modes.set_mode('auto' if auto else 'custom')

        speed = status.get('Current Fan Speed') or status.get('Target Fan Speed')
        if speed is not None:
            try:
                self.slider.set_value(float(speed))
            except ValueError:
                pass

    def _apply(self, _button):
        mode = self.modes.get_mode()
        if mode == 'auto':
            args = ['set', '--auto']
        else:
            speed = '100' if mode == 'max' else str(int(self.slider.get_value()))
            args = ['set', '--speed', speed]

        err = nbfc.apply(args)
        if err:
            self.status_label.set_label(_('Error: {}').format(err))
            return
        self.status_label.set_label(_MODE_SUBTITLE.get(mode, ''))
