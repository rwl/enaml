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

from muntjac.api import Window
from muntjac.application import SingletonApplication

from .muntjac_container import MuntjacContainer

from ..window import AbstractTkWindow


class MuntjacWindow(MuntjacContainer, AbstractTkWindow):
    """ A Muntjac implementation of a Window.

    MuntjacWindow uses a Window to create a simple top level window which
    contains other child widgets and layouts.

    """
    _initializing = False

    #--------------------------------------------------------------------------
    # Setup methods
    #--------------------------------------------------------------------------
    def create(self, parent):
        """ Creates the underlying Muntjac widget.

        """
#        self.widget = MResizingFrame(parent)
        self.widget = Window()
        if parent is not None:
            parent.addComponent(self.widget)
        else:
            app = SingletonApplication.get()
            mw = app.getMainWindow()
            mw.addWindow(self.widget)

    def initialize(self):
        """ Intializes the attributes on the Window.

        """
        self._initializing = True
        try:
            super(MuntjacWindow, self).initialize()
            self.set_title(self.shell_obj.title)
        finally:
            self._initializing = False

    #--------------------------------------------------------------------------
    # Implementation
    #--------------------------------------------------------------------------
    def shell_title_changed(self, title):
        """ The change handler for the 'title' attribute.

        """
        self.set_title(title)

    #--------------------------------------------------------------------------
    # Widget Update Methods
    #--------------------------------------------------------------------------
    def set_title(self, title):
        """ Sets the title of the Window.

        """
        self.widget.setCaption(title)

    def set_visible(self, visible):
        """ Overridden from the parent class to raise the window to
        the front if it should be shown.

        """
        # Don't show the window if we're not initializing.
        if not self._initializing:
            if visible:
                self.widget.setVisible(True)
#                self.widget.raise_()
            else:
                self.widget.setVisible(False)

