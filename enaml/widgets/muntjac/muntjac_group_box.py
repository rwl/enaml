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
from muntjac.ui.themes.base_theme import BaseTheme

from .muntjac_container import MuntjacContainer
#from .muntjac_resizing_widgets import MResizingGroupBox

from ..group_box import AbstractTkGroupBox


class MuntjacGroupBox(MuntjacContainer, AbstractTkGroupBox):
    """ A Muntjac implementation of GroupBox.

    """
    #--------------------------------------------------------------------------
    # Setup methods
    #--------------------------------------------------------------------------
    def create(self, parent):
        """ Creates the underlying Panel control.

        """
#        self.widget = QResizingGroupBox(parent)
        self.widget = Panel()
        parent.addComponent(self.widget)

    def initialize(self):
        """ Intializes the widget with the attributes of this instance.

        """
        super(MuntjacGroupBox, self).initialize()
        shell = self.shell_obj
        self._set_title(shell.title)
        self._set_flat(shell.flat)
        self._set_title_align(shell.title_align)
        self._reset_layout_margins()

    #--------------------------------------------------------------------------
    # Implementation
    #--------------------------------------------------------------------------
    def shell_title_changed(self, title):
        """ Update the title of the group box with the new value from the
        shell object.

        """
        self._set_title(title)
        self._reset_layout_margins()
        # We need to call update constraints since the margins may
        # have changed. Using the size_hint_updated event here is
        # not sufficient.
        self.shell_obj.set_needs_update_constraints()

    def shell_flat_changed(self, flat):
        """ Update the flat flag of the group box with the new value from
        the shell object.

        """
        self._set_flat(flat)
        self._reset_layout_margins()
        # We need to call update constraints since the margins may
        # have changed. Using the size_hint_updated event here is
        # not sufficient.
        self.shell_obj.set_needs_update_constraints()

    def shell_title_align_changed(self, align):
        """ Update the title alignment to the new value from the shell
        object.

        """
        self._set_title_align(align)

    def get_contents_margins(self):
        """ Return the (top, left, right, bottom) margin values for the
        widget.

        """
#        dx, dy, dr, db = self._layout_margins
#        m = self.widget.contentsMargins()
#        contents_margins = (m.top()-dy, m.left()-dx, m.right()-dr, m.bottom()-db)
#        #contents_margins = (m.top(), m.left(), m.right(), m.bottom())
        return (0, 0, 0, 0)

    #--------------------------------------------------------------------------
    # Widget Update methods
    #--------------------------------------------------------------------------
    def _set_title(self, title):
        """ Updates the title of group box.

        """
        self.widget.setCaption(title)

    def _set_flat(self, flat):
        """ Updates the flattened appearance of the group box.

        """
        if flat:
            self.widget.setStyleName(BaseTheme.PANEL_LIGHT)
        else:
            self.widget.removeStyleName(BaseTheme.PANEL_LIGHT)

    def _set_title_align(self, align):
        """ Updates the alignment of the title of the group box.

        """
        pass

