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

from .muntjac_window import MuntjacWindow
from .muntjac_resizing_widgets import MResizingDialog

from ..dialog import AbstractTkDialog


class MuntjacDialog(MuntjacWindow, AbstractTkDialog):
    """ A Muntjac implementation of a Dialog.

    This class creates a simple top-level dialog.

    """
    #--------------------------------------------------------------------------
    # Setup methods
    #--------------------------------------------------------------------------
    def create(self, parent):
        """ Creates the underlying Window control.

        """
#        self.widget = MResizingDialog(parent)
        self.widget = Window()
        parent.addComponent(self.widget)

    def initialize(self):
        """ Intializes the attributes on the QDialog.

        """
        super(MuntjacDialog, self).initialize()
        self.widget.finished.connect(self._on_close)

    #---------------------------------------------------------------------------
    # Implementation
    #---------------------------------------------------------------------------
    def accept(self):
        """ Accept and close the dialog, sending the 'finished' signal.

        """
        self._close_dialog('accepted')

    def reject(self):
        """ Reject and close the dialog, sending the 'finished' signal.

        """
        self._close_dialog('rejected')

    #--------------------------------------------------------------------------
    # Event Handlers
    #--------------------------------------------------------------------------
    def _on_close(self, result):
        """ The event handler for the dialog's finished signal.

        This translates from a QDialog result into an Enaml result enum
        value. The default result is rejection.

        """
        self.reject()

    #--------------------------------------------------------------------------
    # Widget Update Methods
    #--------------------------------------------------------------------------
    def set_visible(self, visible):
        """ Overridden from the parent class to properly launch and close
        the dialog.

        """
        if not self._initializing:
            widget = self.widget
            shell = self.shell_obj
            if visible:
                shell.trait_set(_active=True, opened=True)
                # Muntjac cannot distinguish between app modal and
                # window modal, so we only get one kind.
                widget.setModal(True)
                widget.exec_()
            else:
                self.reject()

    #--------------------------------------------------------------------------
    # Helper Methods
    #--------------------------------------------------------------------------
    def _close_dialog(self, result):
        """ Destroy the dialog, fire events, and set status attributes.

        """
        if self.widget:
            self.widget.close()
        self.shell_obj.trait_set(_result=result, _active=False, closed=result)

