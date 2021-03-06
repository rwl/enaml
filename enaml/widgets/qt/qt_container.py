#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from .qt_component import QtComponent
from .qt_resizing_widgets import QResizingFrame, QResizingWidget

from ..container import AbstractTkContainer


class QtContainer(QtComponent, AbstractTkContainer):
    """ A Qt4 implementation of Container.

    QtContainer is usually to be used as a base class for other container
    widgets. However, it may also be used directly as an undecorated 
    container for widgets for layout purposes.

    """
    def create(self, parent):
        """ Creates the underlying Qt widget.

        """
        self.widget = QResizingFrame(parent)
    
    def bind(self):
        """ Binds the signal handlers for the widget.

        """
        super(QtContainer, self).bind()
        widget = self.widget
        if isinstance(widget, QResizingWidget):
            widget.resized.connect(self.on_resize)

    def on_resize(self):
        """ Triggers a relayout of the shell object since the widget
        has been resized.

        """
        # Notice that we are calling do_layout() here instead of 
        # set_needs_layout() since we want the layout to happen
        # immediately. Otherwise the resize layouts will appear 
        # to lag in the ui. This is a safe operation since by the
        # time we get this resize event, the widget has already 
        # changed size. Further, the only geometry that gets set
        # by the layout manager is that of our children. And should
        # it be required to resize this widget from within the layout
        # call, then the layout manager will do that via invoke_later.
        self.shell_obj.do_layout()

    def size_hint(self):
        """ Returns a (width, height) tuple of integers which represent
        the suggested size of the widget for its current state, ignoring
        any windowing decorations. This value is used by the layout
        manager to determine how much space to allocate the widget.

        """
        size_hint = self.widget.sizeHint()
        return (size_hint.width(), size_hint.height())

    def _reset_layout_margins(self):
        """ Reset the layout margins for this widget.

        """
        super(QtContainer, self)._reset_layout_margins()
        # Now reset our children's layout margins to account for the fact that
        # they have recorded our own margins.
        for child in self.shell_obj.children:
            child.abstract_obj._reset_layout_margins()
