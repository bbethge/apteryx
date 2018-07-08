from gi.repository import Gtk

from search_page import SearchPage
from section_list import SectionList
from view_stack import ViewStack

class Window(Gtk.ApplicationWindow):
    def __init__(self, application, package_cache):
        Gtk.ApplicationWindow.__init__(self, application=application)
        # I18N This is the name of the application.  I pronounce
        # it “apt-er-iks” (like the word “apt”).
        self.set_title(_("Apteryx"))

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.set_title(self.get_title())
        self.set_titlebar(header_bar)

        back_button = Gtk.Button.new_from_icon_name("go-previous",
                                                    Gtk.IconSize.SMALL_TOOLBAR)
        header_bar.pack_start(back_button)

        browse_search_box = Gtk.ButtonBox(Gtk.Orientation.HORIZONTAL)
        browse_search_box.set_layout(Gtk.ButtonBoxStyle.EXPAND)
        header_bar.pack_start(browse_search_box)

        # I18N This is a button to open a view to browse the list
        # of package categories.
        browse_button = Gtk.Button.new_with_label(_("Browse"))
        browse_search_box.add(browse_button)

        # I18N This is a button that shows a search interface.
        search_button = Gtk.Button.new_with_label(_("Search"))
        browse_search_box.add(search_button)

        # I18N This is a button that allows the user to select
        # any Recommended or Suggested packages they want before
        # performing any marked actions (installing, removing,
        # etc.)
        finish_button = Gtk.Button.new_with_label(_("Finish"))
        header_bar.pack_end(finish_button)

        stack = ViewStack()
        stack.go_to_new_page(SectionList(package_cache, stack))
        back_button.connect('clicked', lambda b: stack.go_back())
        browse_button.connect(
            'clicked',
            lambda b:
                stack.go_to_new_page(SectionList(package_cache, stack)))
        search_button.connect(
            'clicked',
            lambda b:
                stack.go_to_new_page(SearchPage(package_cache, stack)))
        self.add(stack)

    def do_realize(self):
        Gtk.ApplicationWindow.do_realize(self)
        css_provider = Gtk.CssProvider()
        # We don’t want the button box to make the header bar taller
        css_provider.load_from_data(b'headerbar > buttonbox {'
                                    b'    padding: 0;'
                                    b'}')
        style_context = self.get_style_context()
        style_context.add_provider_for_screen(
            self.get_screen(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
