from enum import IntEnum
import time

from gi.repository import Gio, GLib, GObject, Gtk

from package_view import PackageView


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
    def __init__(self, package, details_callback):
        super().__init__()
        self.set_orientation(Gtk.Orientation.VERTICAL)

        top_box = Gtk.Box(Gtk.Orientation.HORIZONTAL, 0)
        self.pack_start(top_box, False, False, 0)

        label = Gtk.Label("<b>{}</b>".format(package.name))
        label.set_use_markup(True)
        label.set_xalign(0)
        top_box.pack_start(label, True, True, 0)

        installed_indicator = Gtk.Label(
            # I18N This is a package status.
            _("Installed") if package.is_installed
            # I18N This is a package status.
            else _("Not installed"))
        top_box.pack_start(installed_indicator, False, False, 0)

        button_box = Gtk.ButtonBox(Gtk.Orientation.HORIZONTAL)
        button_box.set_layout(Gtk.ButtonBoxStyle.EXPAND)
        self.pack_start(button_box, False, False, 0)

        # I18N This is a button that opens the detailed package
        # view.
        details_button = Gtk.Button.new_with_label(_("Details"))
        details_button.connect('clicked', details_callback, package)
        button_box.pack_start(details_button, True, True, 0)

        action_button = Gtk.Button.new_with_label(
            # I18N This is a button that removes a package.
            _("Remove") if package.is_installed
            # I18N This is a button that installs a package.
            else _("Install"))
        action_button.set_sensitive(False)
        button_box.pack_start(action_button, True, True, 0)

        self.show_all()


class PackageList(Gtk.Overlay):
    """Displays a list of apt.package.Package objects."""
    # TODO: Synchronize with apt_pkg objects.

    def __init__(self, package_cache, view_stack, package_filter):
        super().__init__()
        self.view_stack = view_stack

        scrolled_window = Gtk.ScrolledWindow()
        self.add(scrolled_window)

        self.spinner = Gtk.Spinner()
        self.spinner.set_no_show_all(True)
        self.spinner.set_halign(Gtk.Align.END)
        self.spinner.set_valign(Gtk.Align.END)
        self.spinner.show()
        self.spinner.start()
        self.add_overlay(self.spinner)

        # Make the spinner bigger
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b'spinner {'
                                    b'    min-width:  32px;'
                                    b'    min-height: 32px;'
                                    b'}')
        style_context = self.spinner.get_style_context()
        style_context.add_provider(css_provider,
                                   Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        package_store = PackageStore(package_cache, package_filter)
        package_store.connect('finished_loading', self.on_finished_loading)
        list_box = Gtk.ListBox.new()
        list_box.bind_model(
            package_store,
            lambda item: PackageListItem(item.package, self.on_details_clicked))
        scrolled_window.add(list_box)

    def on_finished_loading(self, package_store):
        self.spinner.stop()
        self.spinner.hide()

    def on_details_clicked(self, button, package):
        self.view_stack.go_to_new_page(PackageView(package))
