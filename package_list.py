from enum import IntEnum
import time
_ = lambda s: s

import apt_pkg
from gi.repository import Gio, GLib, GObject, Gtk


class PackageWrapper(GObject.Object):
    def __init__(self, package):
        super().__init__()
        self.package = package


class PackageStore(GObject.Object, Gio.ListModel):
    def __init__(self, cache):
        super().__init__()
        self.cache = cache
        self.names = sorted(cache.keys())

    def do_get_item_type(self):
        return PackageWrapper.__gtype__

    def do_get_n_items(self):
        return len(self.cache)

    def do_get_item(self, position):
        return PackageWrapper(self.cache[self.names[position]])


class PackageList(Gtk.Overlay):
    """Displays a list of apt.package.Package objects."""
    # TODO: Synchronize with apt_pkg objects.

    def __init__(self, cache):
        """‘cache’ is an apt.cache.Cache object."""
        super().__init__()

        scrolled_window = Gtk.ScrolledWindow()
        self.add(scrolled_window)

        self.spinner = Gtk.Spinner()
        self.spinner.set_no_show_all(True)
        self.spinner.set_halign(Gtk.Align.END)
        self.spinner.set_valign(Gtk.Align.END)
        self.add_overlay(self.spinner)

        list_box = Gtk.ListBox.new()
        list_box.bind_model(
            PackageStore(cache),
            lambda item: Gtk.Label(item.package.name))
        scrolled_window.add(list_box)
        #package_iter = iter(packages)
        #if self.load_some_packages(package_iter):
        #    self.spinner.show()
        #    self.spinner.start()
        #    GLib.idle_add(lambda: self.load_some_packages(package_iter))

        #name_renderer = Gtk.CellRendererText()
        #name_column = Gtk.TreeViewColumn()
        #name_column.set_title(_("Package name")), 
        #name_column.pack_start(name_renderer, True)
        #name_column.add_attribute(name_renderer, "text", self.Column.NAME)
        #list_view.append_column(name_column)

        #installed_renderer = Gtk.CellRendererToggle()
        #installed_column = Gtk.TreeViewColumn()
        #installed_column.set_title(_("Installed?"))
        #installed_column.pack_start(installed_renderer, False)
        #installed_column.add_attribute(
        #    installed_renderer, "active", self.Column.INSTALLED)
        #list_view.append_column(installed_column)

    #def do_realize(self):
    #    Gtk.Overlay.do_realize(self)
    #    css_provider = Gtk.CssProvider()
    #    # Make the spinner bigger
    #    css_provider.load_from_data(b'spinner {'
    #                                b'    min-width:  32px;'
    #                                b'    min-height: 32px;'
    #                                b'}')
    #    style_context = self.get_style_context()
    #    style_context.add_provider_for_screen(
    #        self.get_screen(),
    #        css_provider,
    #        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
