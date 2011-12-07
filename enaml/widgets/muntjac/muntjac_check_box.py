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

from muntjac.api import CheckBox

from .muntjac_toggle_control import MuntjacToggleControl

from ..check_box import AbstractTkCheckBox


class MuntjacCheckBox(MuntjacToggleControl, AbstractTkCheckBox):
    """ A Muntjac implementation of CheckBox.

    """
    #--------------------------------------------------------------------------
    # Setup methods
    #--------------------------------------------------------------------------
    def create(self, parent):
        """ Creates the underlying CheckBox widget.

        """
        self.widget = CheckBox()
        self.widget.setImmediate(True)
        parent.addComponent(self.widget)

    def bind(self):
        """ Binds the event handlers for the check box.

        """
        super(MuntjacCheckBox, self).bind()
        widget = self.widget
        widget.toggled.connect(self.on_toggled)
        widget.pressed.connect(self.on_pressed)
        widget.released.connect(self.on_released)

