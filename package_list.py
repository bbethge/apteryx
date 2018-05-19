from enum import IntEnum
_ = lambda s: s

import apt_pkg
from gi.repository import GLib, GObject, Gtk


class PackageList(Gtk.Overlay):
    """Displays a list of apt_pkg.Package objects.

    To enable progressive loading of contents, this wraps both a
    Gtk.TreeView and a Gtk.ListStore, which is kept in sync with
    an apt_pkg.Cache object.
    """
    # TODO: Synchronize with apt_pkg objects.

    PACKAGES_TO_LOAD_PER_CYCLE = 100

    class Column(IntEnum):
        NAME      = 0
        INSTALLED = 1

    def __init__(self, packages):
        """
        ‘packages’ may be a generator so that the view may be built
        progressively.
        """
        super().__init__()

        scrolled_window = Gtk.ScrolledWindow()
        self.add(scrolled_window)

        self.spinner = Gtk.Spinner()
        self.spinner.set_no_show_all(True)
        self.spinner.set_halign(Gtk.Align.END)
        self.spinner.set_valign(Gtk.Align.END)
        self.add_overlay(self.spinner)

        model = Gtk.ListStore(GObject.TYPE_STRING, GObject.TYPE_BOOLEAN)
        model.set_sort_column_id(self.Column.NAME, Gtk.SortType.ASCENDING)
        list_view = Gtk.TreeView.new_with_model(model)
        scrolled_window.add(list_view)
        package_iter = iter(packages)
        if self.load_some_packages(package_iter):
            self.spinner.show()
            self.spinner.start()
            GLib.idle_add(lambda: self.load_some_packages(package_iter))

        name_renderer = Gtk.CellRendererText()
        name_column = Gtk.TreeViewColumn()
        name_column.set_title(_("Package name")), 
        name_column.pack_start(name_renderer, True)
        name_column.add_attribute(name_renderer, "text", self.Column.NAME)
        list_view.append_column(name_column)

        installed_renderer = Gtk.CellRendererToggle()
        installed_column = Gtk.TreeViewColumn()
        installed_column.set_title(_("Installed?"))
        installed_column.pack_start(installed_renderer, False)
        installed_column.add_attribute(
            installed_renderer, "active", self.Column.INSTALLED)
        list_view.append_column(installed_column)

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

    def load_some_packages(self, package_iter):
        n_loaded = 0
        model = self.get_child().get_child().get_model()
        # TODO: Limit to a certain computation time, not number of packages
        for package in package_iter:
            if n_loaded == self.PACKAGES_TO_LOAD_PER_CYCLE:
                return True
            model.set(
                model.append(),
                self.Column.NAME,      package.name,
                self.Column.INSTALLED, package.current_state
                                       == apt_pkg.CURSTATE_INSTALLED)
            n_loaded += 1
        self.spinner.stop()
        self.spinner.hide()
        return False
