from enum import Enum, auto

from gi.repository import Gtk


class ViewStack(Gtk.Stack):
    MAX_CHILDREN = 10  # This determines how much history is saved.

    def __init__(self):
        Gtk.Stack.__init__(self)
        self.set_property('height-request', 300)  #FIXME: Compute this

    def go_to_new_page(self, view):
        children = self.get_children()
        visible_child = self.get_visible_child()
        for child in reversed(children):
            if child is visible_child:
                break
            child.destroy()
        children = self.get_children()
        if len(children) == self.MAX_CHILDREN:
            children[0].destroy()
        view.show_all()
        self.add(view)
        self.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT)
        self.set_visible_child(view)

    def go_back(self, n=1):
        children = self.get_children()
        if n+1 > len(children):
            return
        self.set_transition_type(Gtk.StackTransitionType.SLIDE_RIGHT)
        self.set_visible_child(children[-n-1])
