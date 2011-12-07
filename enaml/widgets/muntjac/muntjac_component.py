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

from .muntjac_base_component import MuntjacBaseComponent

from ..component import AbstractTkComponent


class MuntjacComponent(MuntjacBaseComponent, AbstractTkComponent):
    """ A Muntjac implementation of Component.

    A MuntjacComponent is not meant to be used directly. It provides some
    common functionality that is useful to all widgets and should
    serve as the base class for all other classes.

    .. note:: This is not a HasTraits class.

    """
    #: The Muntjac widget created by the component
    widget = None

    #--------------------------------------------------------------------------
    # Setup Methods
    #--------------------------------------------------------------------------
    def create(self, parent):
        """ Creates the underlying Muntjac widget.

        """
        self.widget = Panel()
        parent.addComponent(self.widget)

    def initialize(self):
        """ Initializes the attributes of the Qt widget.

        """
        super(MuntjacComponent, self).initialize()
        shell = self.shell_obj
        self.set_enabled(shell.enabled)
        self.set_visible(shell.visible)

    #--------------------------------------------------------------------------
    # Abstract Implementation
    #--------------------------------------------------------------------------
    @property
    def toolkit_widget(self):
        """ A property that returns the toolkit specific widget for this
        component.

        """
        return self.widget

    def size(self):
        """ Returns the size of the internal toolkit widget, ignoring any
        windowing decorations, as a (width, height) tuple of integers.

        """
        widget = self.widget
        return (widget.getWidth(), widget.getHeight())

    def size_hint(self):
        """ Returns a (width, height) tuple of integers which represent
        the suggested size of the widget for its current state, ignoring
        any windowing decorations. This value is used by the layout
        manager to determine how much space to allocate the widget.

        """
        return self.size()

    def resize(self, width, height):
        """ Resizes the internal toolkit widget according the given
        width and height integers, ignoring any windowing decorations.

        """
        self.widget.setWidth(width)
        self.widget.setHeight(height)

    def min_size(self):
        """ Returns the hard minimum (width, height) of the widget,
        ignoring any windowing decorations. A widget will not be able
        to be resized smaller than this value

        """
        widget = self.widget
        return (widget.getWidth(), widget.getHeight())

    def set_min_size(self, min_width, min_height):
        """ Set the hard minimum width and height of the widget, ignoring
        any windowing decorations. A widget will not be able to be resized
        smaller than this value.

        """
        self.widget.setWidth(min_width)
        self.widget.setHeight(min_height)

    def pos(self):
        """ Returns the position of the internal toolkit widget as an
        (x, y) tuple of integers, including any windowing decorations.
        The coordinates should be relative to the origin of the widget's
        parent, or to the screen if the widget is toplevel.

        """
        widget = self.widget
        return (widget.getPositionX(), widget.getPositionY())

    def move(self, x, y):
        """ Moves the internal toolkit widget according to the given
        x and y integers which are relative to the origin of the
        widget's parent and includes any windowing decorations.

        """
        self.widget.setPositionX(x)
        self.widget.setPositionY(y)

    def frame_geometry(self):
        """ Returns an (x, y, width, height) tuple of geometry info
        for the internal toolkit widget, including any windowing
        decorations.

        """
        widget = self.widget
        x = widget.getPositionX()
        y = widget.getPositionY()
        width = widget.getWidth()
        height = widget.getHeight()
        return (x, y, width, height)

    def geometry(self):
        """ Returns an (x, y, width, height) tuple of geometry info
        for the internal toolkit widget, ignoring any windowing
        decorations.

        """
        widget = self.widget
        x = widget.getPositionX()
        y = widget.getPositionY()
        width = widget.getWidth()
        height = widget.getHeight()
        return (x, y, width, height)

    def set_geometry(self, x, y, width, height):
        """ Sets the geometry of the internal widget to the given
        x, y, width, and height values, ignoring any windowing
        decorations.

        """
        widget = self.widget
        widget.setPositionX(x)
        widget.setPositionY(y)
        widget.setWidth(width)
        widget.setHeight(height)

    #--------------------------------------------------------------------------
    # Shell Object Change Handlers
    #--------------------------------------------------------------------------
    def shell_enabled_changed(self, enabled):
        """ The change handler for the 'enabled' attribute on the shell
        object.

        """
        self.set_enabled(enabled)

    def shell_visible_changed(self, visible):
        """ The change handler for the 'visible' attribute on the shell
        object.

        """
        self.set_visible(visible)

    def shell_bg_color_changed(self, color):
        """ The change handler for the 'bg_color' attribute on the shell
        object. Sets the background color of the internal widget to the
        given color.

        """
        self.set_bg_color(color)

    def shell_fg_color_changed(self, color):
        """ The change handler for the 'fg_color' attribute on the shell
        object. Sets the foreground color of the internal widget to the
        given color.

        """
        self.set_fb_color(color)

    def shell_font_changed(self, font):
        """ The change handler for the 'font' attribute on the shell
        object. Sets the font of the internal widget to the given font.

        """
        self.set_font(font)

    #--------------------------------------------------------------------------
    # Widget Update Methods
    #--------------------------------------------------------------------------
    def set_enabled(self, enabled):
        """ Enable or disable the widget.

        """
        self.widget.setEnabled(enabled)

    def set_visible(self, visible):
        """ Show or hide the widget.

        """
        self.shell_obj.parent.set_needs_update_constraints()
        self.widget.setVisible(visible)

    def set_bg_color(self, color):
        """ Set the background color of the widget.

        """
        pass

    def set_fg_color(self, color):
        """ Set the foreground color of the widget.

        """
        pass

    def set_font(self, font):
        """ Set the font of the underlying toolkit widget to an
        appropriate QFont.

        """
        pass

    #--------------------------------------------------------------------------
    # Convenienence methods
    #--------------------------------------------------------------------------

    def child_widgets(self):
        """ Iterates over the shell widget's children and yields the
        toolkit widgets for those children.

        """
        for child in self.shell_obj.children:
            yield child.toolkit_widget

    def _get_layout_margins(self, widget):
        """ Compute the size of the margins between the layout rectangle and the
        widget drawing rectangle.

        """
        pass

    def _reset_layout_margins(self):
        """ Reset the layout margins for this widget.

        """
        pass
