from enum import IntEnum
import time
_ = lambda s: s

from gi.repository import Gio, GLib, GObject, Gtk


class PackageWrapper(GObject.Object):
    def __init__(self, package):
        super().__init__()
        self.package = package


class PackageStore(GObject.Object, Gio.ListModel):
    PACKAGE_LOAD_CYCLE_TIME = 0.05

    __gsignals__ = {
        'finished_loading': (GObject.SIGNAL_RUN_FIRST, None, ()) }

    def __init__(self, package_cache, package_filter):
        super().__init__()
        self.package_filter = package_filter
        self.packages = []
        self.package_iter = iter(package_cache)
        GLib.idle_add(self.load_some_packages)

    def load_some_packages(self):
        end_time = time.perf_counter() + self.PACKAGE_LOAD_CYCLE_TIME
        position = len(self.packages)
        finished = False
        for package in self.package_iter:
            if self.package_filter(package):
                self.packages.append(package)
            if time.perf_counter() >= end_time:
                break
        else:
            finished = True
        if len(self.packages) > position:
            self.items_changed(position, 0, len(self.packages) - position)
        if finished:
            self.emit('finished_loading')
            return GLib.SOURCE_REMOVE
        return GLib.SOURCE_CONTINUE

    def do_get_item_type(self):
        return PackageWrapper.__gtype__

    def do_get_n_items(self):
        return len(self.packages)

    def do_get_item(self, position):
        return PackageWrapper(self.packages[position])


class PackageListItem(Gtk.Box):
    def __init__(self, package):
        super().__init__()
        self.set_orientation(Gtk.Orientation.HORIZONTAL)

        label = Gtk.Label(package.name)
        label.set_xalign(0)
        label.show()
        self.pack_start(label, True, True, 0)

        installed_indicator = Gtk.Label(
            _("Installed") if package.is_installed else _("Not Installed"))
        installed_indicator.show()
        self.pack_start(installed_indicator, False, False, 0)


class PackageList(Gtk.Overlay):
    """Displays a list of apt.package.Package objects."""
    # TODO: Synchronize with apt_pkg objects.

    def __init__(self, package_cache, package_filter):
        super().__init__()

        scrolled_window = Gtk.ScrolledWindow()
        self.add(scrolled_window)

        self.spinner = Gtk.Spinner()
        self.spinner.set_no_show_all(True)
        self.spinner.set_halign(Gtk.Align.END)
        self.spinner.set_valign(Gtk.Align.END)
        self.spinner.show()
        self.spinner.start()
        self.add_overlay(self.spinner)

        package_store = PackageStore(package_cache, package_filter)
        package_store.connect('finished_loading', self.on_finished_loading)
        list_box = Gtk.ListBox.new()
        list_box.bind_model(
            package_store,
            lambda item: PackageListItem(item.package))
        scrolled_window.add(list_box)

    def on_finished_loading(self, package_store):
        self.spinner.stop()
        self.spinner.hide()

    def do_realize(self):
        Gtk.Overlay.do_realize(self)
        css_provider = Gtk.CssProvider()
        # Make the spinner bigger
        css_provider.load_from_data(b'spinner {'
                                    b'    min-width:  32px;'
                                    b'    min-height: 32px;'
                                    b'}')
        style_context = self.get_style_context()
        style_context.add_provider_for_screen(
            self.get_screen(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
