#------------------------------------------------------------------------------
# Copyright (C) 2011 Enthought, Inc.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------------

from muntjac.api import Panel

from .muntjac_component import MuntjacComponent
#from .muntjac_resizing_widgets import MResizingFrame, MResizingWidget

from ..container import AbstractTkContainer


class MuntjacContainer(MuntjacComponent, AbstractTkContainer):
    """ A Muntjac implementation of Container.

    MuntjacContainer is usually to be used as a base class for other
    container widgets. However, it may also be used directly as an
    undecorated container for widgets for layout purposes.

    """
    def create(self, parent):
        """ Creates the underlying Muntjac widget.

        """
#        self.widget = MResizingFrame(parent)
        self.widget = Panel()
        if parent is not None:
            parent.addComponent(self.widget)

    def bind(self):
        """ Binds the signal handlers for the widget.

        """
        super(MuntjacContainer, self).bind()
#        widget = self.widget
#        if isinstance(widget, MResizingWidget):
#            widget.resized.connect(self.on_resize)

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
        widget = self.widget
        return (widget.getWidth(), widget.getHeight())

    def _reset_layout_margins(self):
        """ Reset the layout margins for this widget.

        """
        super(MuntjacContainer, self)._reset_layout_margins()
        # Now reset our children's layout margins to account for the fact that
        # they have recorded our own margins.
        for child in self.shell_obj.children:
            child.abstract_obj._reset_layout_margins()
