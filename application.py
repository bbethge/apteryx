import gi
from gi.repository import Gtk, Gio

import apt

from window import Window

class Application(Gtk.Application):
    def __init__(self):
        # TODO: Set application ID when we have a domain name
        super().__init__(application_id=None,
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        cache = apt.Cache()
        window = Window(self, cache)
        window.show_all()
