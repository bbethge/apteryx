from gi.repository import Gdk, GObject, Gtk

from package_list import PackageList
from pgettext import pgettext


class SearchPage(Gtk.Grid):
    MT = Gdk.ModifierType
    # Modifiers that cause us to ignore the return key instead of
    # activating.
    _MODIFIERS = (MT.SHIFT_MASK | MT.CONTROL_MASK | MT.BUTTON1_MASK
                  | MT.BUTTON2_MASK | MT.BUTTON3_MASK | MT.BUTTON4_MASK
                  | MT.BUTTON5_MASK | MT.SUPER_MASK | MT.HYPER_MASK
                  | MT.META_MASK)
    del MT

    def __init__(self, package_cache, view_stack):
        super().__init__()
        self._package_cache = package_cache
        self._view_stack = view_stack

        self._text_view = Gtk.TextView()
        self._text_view.set_hexpand(True)
        self._text_view.set_vexpand(True)
        self._text_view.set_accepts_tab(False)
        self.attach(self._text_view, 0, 0, 1, 1)
        self._text_view.connect('map', lambda tv: tv.grab_focus())
        # TODO: Use a keybinding
        self._text_view.connect('key-press-event',
                                self._on_text_view_key_press)

        button = Gtk.Button(pgettext("Search page", "Go"))
        button.set_hexpand(True)
        button.set_can_default(True)
        self.attach_next_to(button, self._text_view, Gtk.PositionType.BOTTOM,
                            1, 1)
        button.connect('map', lambda b: b.grab_default())
        button.connect('clicked', self._on_button_clicked)

    def _on_button_clicked(self, button):
        text_buf = self._text_view.get_buffer()
        search = text_buf.get_text(text_buf.get_start_iter(),
                                   text_buf.get_end_iter(), False)
        if search != '':
            package_list = PackageList(self._package_cache, self._view_stack,
                                       lambda p: p.name.find(search) != -1)
            self._view_stack.go_to_new_page(package_list)

    def _on_text_view_key_press(self, text_view, event):
        if (event.keyval == Gdk.KEY_Return
                and not event.state & self._MODIFIERS):
            toplevel = text_view.get_toplevel()
            if isinstance(toplevel, Gtk.Window):
                toplevel.activate_default()
            return True
        else:
            return False
