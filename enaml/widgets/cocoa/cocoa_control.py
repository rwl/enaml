import functools

from .cocoa_component import CocoaComponent

from ..control import AbstractTkControl


class CocoaControl(CocoaComponent, AbstractTkControl):

    def size_hint(self):
        """ Returns a (width, height) tuple of integers which represent
        the suggested size of the widget for its current state. This 
        value is used by the layout manager to determine how much 
        space to allocate the widget.

        """
        width, height = self.widget.cell().cellSize()
        print self, width, height
        return (width, height)
