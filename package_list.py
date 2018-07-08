import time

from gi.repository import GLib, Gtk

from package_view import PackageView


class _PackageListItem(Gtk.Box):
    def __init__(self, package, details_callback):
        super().__init__()
        self.set_orientation(Gtk.Orientation.VERTICAL)

        top_box = Gtk.Box(Gtk.Orientation.HORIZONTAL, 0)
        self.pack_start(top_box, False, False, 0)

        label = Gtk.Label(f'<b>{package.name}</b>')
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

    PACKAGE_LOAD_CYCLE_TIME = 0.05

    def __init__(self, package_cache, view_stack, package_filter):
        super().__init__()
        self._view_stack = view_stack

        self._package_filter = package_filter
        self._packages = []
        self._package_iter = iter(package_cache)

        scrolled_window = Gtk.ScrolledWindow()
        self.add(scrolled_window)

        self._spinner = Gtk.Spinner()
        self._spinner.set_no_show_all(True)
        self._spinner.set_halign(Gtk.Align.END)
        self._spinner.set_valign(Gtk.Align.END)
        self._spinner.show()
        self._spinner.start()
        self.add_overlay(self._spinner)

        # Make the spinner bigger
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b'spinner {'
                                    b'    min-width:  32px;'
                                    b'    min-height: 32px;'
                                    b'}')
        style_context = self._spinner.get_style_context()
        style_context.add_provider(css_provider,
                                   Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self._list_box = Gtk.ListBox.new()
        scrolled_window.add(self._list_box)

        GLib.idle_add(self._load_some_packages)

    def _load_some_packages(self):
        end_time = time.perf_counter() + self.PACKAGE_LOAD_CYCLE_TIME
        position = len(self._packages)
        finished = False
        for package in self._package_iter:
            if self._package_filter(package):
                self._list_box.insert(
                    _PackageListItem(package, self._on_details_clicked),
                    len(self._packages))
                self._packages.append(package)
            if time.perf_counter() >= end_time:
                break
        else:
            finished = True
        if finished:
            self._on_finished_loading()
            return GLib.SOURCE_REMOVE
        return GLib.SOURCE_CONTINUE

    def _on_finished_loading(self):
        self._spinner.stop()
        self._spinner.hide()

    def _on_details_clicked(self, button, package):
        self._view_stack.go_to_new_page(PackageView(package))
