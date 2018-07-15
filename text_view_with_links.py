import subprocess

import gi
from gi.repository import Gdk, Gtk, Pango


class TextViewWithLinks(Gtk.TextView):
    """
        Based on the Text View Hypertext demo from gtk3-demo, this
        implements a Gtk.TextView that can contain external links.
        Unlike the demo, it does not provide internal links that can be
        used to display a different page in the TextView.  It may not
        work very well with the “editable” property set.
    """

    def __init__(self):
        super().__init__()
        self._hovering = False
        self.connect('event-after', type(self)._on_event_after)

    def insert_link(self, iter, text, url):
        """
            Insert a link into our buffer at “iter” which will be
            displayed with text “text” and will have the URL “url”
            as its target.
        """
        buf = self.get_buffer()
        tag = buf.create_tag(None, foreground='blue',
                             underline=Pango.Underline.SINGLE)
        tag.url = url
        buf.insert_with_tags(iter, text, tag)

    def follow_if_link(self, iter):
        """
            Look at all tags covering the position of “iter” in the
            text view, and if one of them is a link, launch an external
            browser to view it.
        """
        for tag in iter.get_tags():
            if hasattr(tag, 'url'):
                # Note that xdg-open will show a dialog if it does not
                # support the link.
                # TODO: Recover if xdg-open is not found.
                subprocess.run(['xdg-open', tag.url])

    def do_realize(self):
        # NOTE: For some reason super() does not work here.
        Gtk.TextView.do_realize(self)
        display = self.get_display()
        self._hand_cursor = Gdk.Cursor.new_from_name(display, "pointer")
        self._regular_cursor = Gdk.Cursor.new_from_name(display, "text")

    def do_unrealize(self):
        del self._hand_cursor
        del self._regular_cursor
        Gtk.TextView.do_unrealize(self)

    def do_key_press_event(self, event):
        if event.keyval in [Gdk.KEY_Return, Gdk.KEY_KP_Enter]:
            buf = self.get_buffer()
            iter = buf.get_iter_at_mark(buf.get_insert())
            self.follow_if_link(iter)
        return Gtk.TextView.do_key_press_event(self, event)

    def do_motion_notify_event(self, event):
        x, y = self.window_to_buffer_coords(Gtk.TextWindowType.TEXT,
                                            event.x, event.y)
        self._set_cursor_if_appropriate(x, y)
        return Gtk.TextView.do_motion_notify_event(self, event)

    def _on_event_after(self, event):
        if event.type == Gdk.EventType.BUTTON_RELEASE:
            if event.button.button != Gdk.BUTTON_PRIMARY:
                return
            ex = event.button.x
            ey = event.button.y
        elif event.type == Gdk.EventType.TOUCH_END:
            ex = event.touch.x
            ey = event.touch.y
        else:
            return
        buf = self.get_buffer()
        # The method used in the demo to avoid following links if there
        # is a selection won’t work anyway, so don’t worry about it.
        x, y = self.window_to_buffer_coords(Gtk.TextWindowType.TEXT, ex, ey)
        over_text, it = self.get_iter_at_location(x, y)
        if over_text:
            self.follow_if_link(it)

    def _set_cursor_if_appropriate(self, x, y):
        hovering = False
        over_text, it = self.get_iter_at_location(x, y)
        if over_text:
            for tag in it.get_tags():
                if hasattr(tag, 'url'):
                    hovering = True
                    break
        if hovering != self._hovering:
            self._hovering = hovering
            window = self.get_window(Gtk.TextWindowType.TEXT)
            if self._hovering:
                window.set_cursor(self._hand_cursor)
            else:
                window.set_cursor(self._regular_cursor)
