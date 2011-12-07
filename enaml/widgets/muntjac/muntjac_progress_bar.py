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

from muntjac.api import ProgressIndicator

from .muntjac_control import MuntjacControl

from ..progress_bar import AbstractTkProgressBar


class MuntjacProgressBar(MuntjacControl, AbstractTkProgressBar):
    """ Muntjac implementation of ProgressBar.

    """
    #--------------------------------------------------------------------------
    # Setup Methods
    #--------------------------------------------------------------------------
    def create(self, parent):
        """ Creates the underlying ProgressIndicator.

        """
        self.widget = ProgressIndicator()
        parent.addComponent(self.widget)

    def initialize(self):
        """ Initialize the attributes of the progress bar.

        """
        super(MuntjacControl, self).initialize()
        self.widget.setIndeterminate(False)
        shell = self.shell_obj
        self._set_minimum(shell.minimum)
        self._set_maximum(shell.maximum)
        self._set_value(shell.value)

    #--------------------------------------------------------------------------
    # Abstract Implementation Methods
    #--------------------------------------------------------------------------
    def shell_value_changed(self, value):
        """ The change handler for the 'value' attribute of the shell
        object.

        """
        self._set_value(value)

    def shell_minimum_changed(self, minimum):
        """ The change handler for the 'minimum' attribute of the shell
        object.

        """
        self._set_minimum(minimum)

    def shell_maximum_changed(self, maximum):
        """ The change handler for the 'maximum' attribute of the shell
        object

        """
        self._set_maximum(maximum)

    #--------------------------------------------------------------------------
    # Widget Update Methods
    #--------------------------------------------------------------------------
    def _set_value(self, value):
        """ Sets the value of the progress bar.

        """
        minimum = self.shell_obj.minimum
        maximum = self.shell_obj.maximum
        new_val = value / (maximum - minimum)  # normalise: 0.0 - 1.0
        self.widget.setValue(new_val)

    def _set_minimum(self, minimum):
        """ Sets the minimum value of the progress bar.

        """
        pass

    def _set_maximum(self, maximum):
        """ Sets the maximum value of the progress bar.

        """
        pass

