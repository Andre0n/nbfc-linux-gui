import math

from gi.repository import Gdk, Gtk

import cairo


class FanWidget(Gtk.DrawingArea):
    """Spinning fan visual: blue petal blades, progress arc, centered percent.

    Rotation speed follows the fan speed percent.
    """

    BLADES = 8
    MAX_DEG_PER_SEC = 360       # rotation velocity at 100%
    EDGE_MARGIN = 4             # px between widget edge and outer ring

    TRACK_WIDTH = 8             # grey background ring
    ARC_WIDTH = 8               # blue progress arc
    TRACK_RGBA = (0.5, 0.5, 0.5, 0.35)
    ACCENT_RGB = (0.21, 0.52, 0.89)   # #3584e4

    PETAL_INNER_FRAC = 0.50     # petal root radius, fraction of radius
    PETAL_TIP_FRAC = 0.9       # petal tip radius, fraction of radius
    PETAL_SWEEP = 0.45         # tip leads root by this angle (radians) -> curved blade
    PETAL_ROOT_W = 0.10        # blade half-width at root (radians)
    PETAL_TIP_W = 0.22         # blade half-width at tip (radians)
    LABEL_FONT_FRAC = 0.25      # font size as fraction of radius

    HUB_FRAC = 0.42            # hub disc radius, fraction of radius

    def __init__(self, size: int = 180) -> None:
        super().__init__()
        self.set_content_width(size)
        self.set_content_height(size)
        self.set_draw_func(self._draw)

        self.angle: float = 0.0          # radians
        self.deg_per_sec: float = 0.0    # current rotation velocity
        self.percent: float = 0.0        # last set speed percent
        self._last: int | None = None    # last frame time (microseconds)

        self.add_tick_callback(self._on_tick)

    def set_speed(self, percent: float) -> None:
        """percent 0-100 -> rotation velocity. 0 stops, 100 spins fast."""
        self.percent = max(0.0, min(percent, 100))
        # ponytail: linear map, tune MAX_DEG_PER_SEC if it looks too fast/slow
        self.deg_per_sec = self.percent / 100 * self.MAX_DEG_PER_SEC

    def _on_tick(self, _widget: Gtk.Widget, frame_clock: Gdk.FrameClock) -> bool:
        now = frame_clock.get_frame_time()  # microseconds
        if self._last is not None:
            dt = (now - self._last) / 1_000_000
            self.angle += math.radians(self.deg_per_sec) * dt
            self.angle %= 2 * math.pi
        self._last = now
        self.queue_draw()
        return True  # keep ticking

    def _draw(self, _area: Gtk.DrawingArea, cr: cairo.Context,
              width: int, height: int) -> None:
        cx, cy = width / 2, height / 2
        radius = min(width, height) / 2 - self.EDGE_MARGIN
        fg = self.get_color()  # theme foreground, adapts light/dark
        self._draw_track(cr, cx, cy, radius)
        self._draw_arc(cr, cx, cy, radius)
        self._draw_blades(cr, cx, cy, radius)
        self._draw_hub(cr, cx, cy, radius, fg)
        self._draw_label(cr, cx, cy, radius, fg)

    def _draw_track(self, cr, cx, cy, radius) -> None:
        cr.set_source_rgba(*self.TRACK_RGBA)
        cr.set_line_width(self.TRACK_WIDTH)
        cr.arc(cx, cy, radius, 0, 2 * math.pi)
        cr.stroke()

    def _draw_arc(self, cr, cx, cy, radius) -> None:
        # Blue progress arc, from top, clockwise, proportional to percent.
        sweep = self.percent / 100 * 2 * math.pi
        if sweep <= 0:
            return
        start = -math.pi / 2
        cr.set_source_rgb(*self.ACCENT_RGB)
        cr.set_line_width(self.ARC_WIDTH)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.arc(cx, cy, radius, start, start + sweep)
        cr.stroke()

    def _draw_blades(self, cr, cx, cy, radius) -> None:
        cr.set_source_rgb(*self.ACCENT_RGB)
        inner = radius * self.PETAL_INNER_FRAC
        tip = radius * self.PETAL_TIP_FRAC
        for i in range(self.BLADES):
            a = self.angle + i * 2 * math.pi / self.BLADES
            self._petal(cr, cx, cy, a, inner, tip)

    def _petal(self, cr, cx, cy, a, inner, tip) -> None:
        # Swept blade: narrow curved root, wider tip that leads by PETAL_SWEEP.
        def pt(r, ang):
            return cx + r * math.cos(ang), cy + r * math.sin(ang)

        sweep = self.PETAL_SWEEP
        mid = (inner + tip) / 2
        root_l = pt(inner, a - self.PETAL_ROOT_W)
        root_r = pt(inner, a + self.PETAL_ROOT_W)
        tip_l = pt(tip, a + sweep - self.PETAL_TIP_W)
        tip_r = pt(tip, a + sweep + self.PETAL_TIP_W)
        c_lead = pt(mid, a + sweep * 0.5 - self.PETAL_ROOT_W)   # curved leading edge
        c_trail = pt(mid, a + sweep * 0.5 + self.PETAL_TIP_W)   # curved trailing edge
        cr.move_to(*root_l)
        cr.curve_to(*c_lead, *c_lead, *tip_l)   # leading edge out to tip
        cr.line_to(*tip_r)                       # across the tip
        cr.curve_to(*c_trail, *c_trail, *root_r)  # trailing edge back to root
        cr.close_path()
        cr.fill()

    def _draw_hub(self, cr, cx, cy, radius, fg) -> None:
        # Central cap the number sits on. Theme fg at low alpha:
        # light disc in light theme, faint disc in dark theme.
        hub_r = radius * self.HUB_FRAC
        cr.set_source_rgba(fg.red, fg.green, fg.blue, 0.1)
        cr.arc(cx, cy, hub_r, 0, 2 * math.pi)
        cr.fill()

    def _draw_label(self, cr, cx, cy, radius, fg) -> None:
        # Percent, centered. Theme fg -> readable on the tinted hub.
        text = f'{self.percent:.0f}%'
        cr.set_source_rgb(fg.red, fg.green, fg.blue)
        cr.select_font_face('Sans', cairo.FONT_SLANT_NORMAL,
                            cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(radius * self.LABEL_FONT_FRAC)
        extents = cr.text_extents(text)
        cr.move_to(cx - extents.width / 2 - extents.x_bearing,
                   cy - extents.height / 2 - extents.y_bearing)
        cr.show_text(text)
