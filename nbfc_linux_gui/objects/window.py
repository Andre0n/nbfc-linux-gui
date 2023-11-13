import subprocess
from subprocess import PIPE

from gi.repository import Gtk

MAIN_BOX_PADDING = 16
MAIN_BOX_SPACING = 10


class MainWindow(Gtk.ApplicationWindow):

    is_current_active = False
    css_data = """
    .speed-controls-label {
        font-size: 24px;
        font-weight: bold;
    }
    .custom-label {
        font-size: 18px;
    }

    .switch {
        cursor: pointer;
    }
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_default_size(600, 400)
        self.set_resizable(False)
        self.set_title('NoteBook FanControl GUI')

        self.css_provider = Gtk.CssProvider()
        self.css_provider.load_from_data(self.css_data.encode())

        # Main Box
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.main_box.set_spacing(MAIN_BOX_SPACING)
        self.main_box.set_margin_top(MAIN_BOX_PADDING)
        self.main_box.set_margin_start(MAIN_BOX_PADDING)
        self.main_box.set_margin_end(MAIN_BOX_PADDING)
        self.set_child(self.main_box)

        self.speed_controls_label = Gtk.Label(
            label='Speed Controls', css_classes=['speed-controls-label']
        )
        self.speed_controls_label.set_halign(Gtk.Align.START)
        self.speed_controls_label.get_style_context().add_provider(
            self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.main_box.append(self.speed_controls_label)

        self.current_speed_label = Gtk.Label(
            label='Current Speed: system defined'
        )
        self.current_speed_label.set_hexpand(True)
        self.current_speed_label.set_halign(Gtk.Align.START)
        self.current_speed_label.set_css_classes(['custom-label'])
        self.current_speed_label.get_style_context().add_provider(
            self.css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        self.main_box.append(self.current_speed_label)

        # Switch Automatic Fan Control
        self.switch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.switch = Gtk.Switch()
        self.switch.set_active(False)
        self.switch_box.append(self.switch)

        self.switch_label = Gtk.Label(label='Auto')
        self.switch_box.append(self.switch_label)
        self.switch_box.set_spacing(5)

        self.main_box.append(self.switch_box)

        # Speed Control Slider
        self.slider = Gtk.Scale()
        self.slider.set_digits(0)
        self.slider.set_range(10, 100)
        self.slider.set_draw_value(True)
        self.slider.set_value(50)

        self.main_box.append(self.slider)

        # Apply changes Button
        self.apply_button = Gtk.Button(label='Apply')
        self.apply_button.connect('clicked', self.apply_button_clicked)
        self.main_box.append(self.apply_button)

    def apply_button_clicked(self, _):
        if self.switch.get_active():
            if not self.is_current_active:
                subprocess.Popen(
                    ['pkexec', 'nbfc', 'set', '--auto'],
                    stdout=PIPE,
                    stderr=PIPE,
                )
                self.is_current_active = True
                self.current_speed_label.set_label('Current Speed: auto')
        else:
            slider_value = str(self.slider.get_value())
            subprocess.Popen(
                ['pkexec', 'nbfc', 'set', '--speed', slider_value],
                stdout=PIPE,
                stderr=PIPE,
            )
            self.is_current_active = False
            self.switch.set_active(False)
            self.current_speed_label.set_label(
                f'Current Speed: {slider_value}%'
            )
