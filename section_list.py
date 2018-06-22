from enum import IntEnum

import apt
import apt.cache
from gi.repository import GLib, GObject, Gtk, Pango
from gi.repository.GdkPixbuf import Pixbuf

from package_list import PackageList


sections = [  # From Debian policy manual version 4.1.3.0
    # section name    icon name                     display name
    ('admin',         None,                       _("Administration")),
    ('cli-mono',      None,                       _("CLI/Mono")),
    ('comm',          None,                       _("Communication Devices")),
    ('database',      None,                       _("Databases and Tools")),
    ('debug',         None,                       _("Debugging Symbols")),
    ('devel',         'applications-development', _("Software Development")),
    ('doc',           None,                       _("Documentation")),
    ('editors',       'text-editor',              _("Text Editors")),
    ('education',     None,                       _("Education")),
    ('electronics',   None,                       _("Electronics")),
    ('embedded',      None,                       _("Embedded Systems")),
    ('fonts',         'applications-fonts',       _("Fonts")),
    ('games',         'applications-games',       _("Games")),
    ('gnome',         'gnome-foot',               _("G<span size='smaller'>NOME</span>")),
    ('gnu-r',         None,                       _("R <span size='smaller'>(Programming Language)</span>")),
    ('gnustep',       None,                       _("The GNUstep Environment")),
    ('graphics',      'applications-graphics',    _("Graphics")),
    ('hamradio',      None,                       _("Ham Radio")),
    ('haskell',       None,                       _("Haskell <span size='smaller'>(Programming Language)</span>")),
    ('httpd',         None,                       _("Web Servers")),
    ('interpreters',  None,                       _("Interpreted Programming Languages")),
    ('introspection', None,                       _("Introspection")),
    ('java',          None,                       _("Java <span size='smaller'>(Programming Language)</span>")),
    ('javascript',    None,                       _("JavaScript <span size='smaller'>(Programming Language)</span>")),
    ('kde',           None,                       _("KDE Desktop Environment")),
    ('kernel',        None,                       _("Kernel")),
    ('libdevel',      None,                       _("Development Files")),
    ('libs',          None,                       _("Software Libraries")),
    ('lisp',          None,                       _("Lisp <span size='smaller'>(Programming Language)</span>")),
    ('localization',  None,                       _("Support for Other Languages")),
    ('mail',          None,                       _("E-mail")),
    ('math',          None,                       _("Mathematics")),
    ('metapackages',  None,                       _("Metapackages")),
    ('misc',          None,                       _("Miscellaneous")),
    ('net',           'applications-internet',    _("Network Services")),
    ('news',          None,                       _("Usenet")),
    ('ocaml',         None,                       _("OCaml <span size='smaller'>(Programming Language)</span>")),
    ('oldlibs',       None,                       _("Obsolete Software Libraries")),
    ('otherosfs',     None,                       _("Software to Read Foreign Filesystems")),
    ('perl',          None,                       _("Perl <span size='smaller'>(Programming Language)</span>")),
    ('php',           None,                       _("PHP Hypertext Preprocessor")),
    ('python',        None,                       _("Python <span size='smaller'>(Programming Language)</span>")),
    ('ruby',          None,                       _("Ruby <span size='smaller'>(Programming Language)</span>")),
    ('rust',          None,                       _("Rust")),
    ('science',       'applications-science',     _("Science")),
    ('shells',        'terminal',                 _("Commandline Shells")),
    ('sound',         'applications-multimedia',  _("Sound")),
    ('tasks',         None,                       _("Tasks")),
    ('tex',           None,                       _("T<sub>E</sub>Χ")),
    ('text',          None,                       _("Text Processing")),
    ('utils',         'applications-utilities',   _("Utilities")),
    ('vcs',           None,                       _("Version Control Systems")),
    ('video',         'applications-multimedia',  _("Video")),
    ('web',           'applications-internet',    _("Web")),
    ('x11',           None,                       _("X Window System")),
    ('xfce',          None,                       _("X<span size='smaller'>FCE</span> Desktop Environment")),
    ('zope',          None,                       _("Zope/Plone Framework"))]

# TODO: support high DPI
# FIXME: have to set wrap width manually but it should be automatically computed
ICON_SIZE  = 64
WRAP_WIDTH = 96


class Store(Gtk.ListStore):
    class Column(IntEnum):
        NAME  = 0
        LABEL = 1
        ICON  = 2

    def __init__(self, screen):
        super().__init__(
            GObject.TYPE_STRING, GObject.TYPE_STRING, Pixbuf.__gtype__)
        icon_theme = Gtk.IconTheme.get_for_screen(screen)
        for section, icon_name, label in sections:
            it = self.append()
            if icon_name is None:
                icon_name = 'applications-other'
            icon = None
            try:
                icon = icon_theme.load_icon(
                    icon_name, ICON_SIZE,
                    Gtk.IconLookupFlags.USE_BUILTIN
                    | Gtk.IconLookupFlags.GENERIC_FALLBACK)
            except GLib.Error as error:
                if error.domain != 'gtk-icon-theme-error-quark':
                    raise
            self.set(it,
                self.Column.NAME,  section,
                self.Column.LABEL, label,
                self.Column.ICON,  icon)
        self.set_sort_column_id(self.Column.LABEL, Gtk.SortType.ASCENDING)


class SectionList(Gtk.ScrolledWindow):
    def __init__(self, package_cache, view_stack):
        super().__init__()
        self.package_cache = package_cache
        self.view_stack    = view_stack
        icon_view          = Gtk.IconView()
        icon_view.set_activate_on_single_click(True)
        icon_view.set_item_width(WRAP_WIDTH)
        icon_view.connect('item-activated', self.do_item_activated)
        self.add(icon_view)

    def do_screen_changed(self, previous_screen):
        screen = self.get_screen()
        if screen is not None:
            icon_view = self.get_child()
            icon_view.set_model(Store(screen))
            icon_view.set_markup_column(Store.Column.LABEL)
            icon_view.set_pixbuf_column(Store.Column.ICON)

    def do_item_activated(self, icon_view, path):
        model = icon_view.get_model()
        section = model.get_value(model.get_iter(path), model.Column.NAME)
        package_view = PackageList(
            self.package_cache, self.view_stack,
            lambda p: p.section.rsplit('/')[-1] == section)
        self.view_stack.go_to_new_page(package_view)
