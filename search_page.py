from gi.repository import Gtk

from package_list import PackageList
from pgettext import pgettext


class SearchPage(Gtk.Grid):
    def __init__(self, package_cache, view_stack):
        super().__init__()
        self._package_cache = package_cache
        self._view_stack = view_stack

        self._text_view = Gtk.TextView()
        self._text_view.set_hexpand(True)
        self._text_view.set_vexpand(True)
        self.attach(self._text_view, 0, 0, 1, 1)

        button = Gtk.Button(pgettext("Search page", "Go"))
        button.set_hexpand(True)
        self.attach_next_to(button, self._text_view, Gtk.PositionType.BOTTOM,
                            1, 1)
        button.connect('clicked', self._on_search_button_clicked)

    def _on_search_button_clicked(self, button):
        text_buf = self._text_view.get_buffer()
        search = text_buf.get_text(text_buf.get_start_iter(),
                                   text_buf.get_end_iter(), False)
        if search != '':
            package_list = PackageList(self._package_cache, self._view_stack,
                                       lambda p: p.name.find(search) != -1)
            self._view_stack.go_to_new_page(package_list)
