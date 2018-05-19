import gi
from gi.repository import Gtk, Gio

import apt_pkg

from window import Window

class Application(Gtk.Application):
    def __init__(self):
        # TODO: change application ID before release
        super().__init__(application_id='org.example.apteryx',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        cache = apt_pkg.Cache()
        window = Window(self, cache)
        window.show_all()
