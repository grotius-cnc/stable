#!/usr/bin/env python
class Widgets:

    def __init__(self, builder):
        self._builder = builder

    def __getattr__(self, attr):
        widget = self._builder.get_object(attr)
        if widget is None:
            raise AttributeError, "No widget %widget" % attr
            raise IndexError, "No widget %widget" % attr
        return widget
