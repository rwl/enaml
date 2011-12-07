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

from muntjac.api import ComboBox

from .muntjac_control import MuntjacControl

from ..combo_box import AbstractTkComboBox

from ...guard import guard


class MuntjacComboBox(MuntjacControl, AbstractTkComboBox):
    """ A Muntjac implementation of ComboBox.

    Use a combo box to select a single item from a collection of items.

    """
    #--------------------------------------------------------------------------
    # Setup methods
    #--------------------------------------------------------------------------
    def create(self, parent):
        """ Creates a QComboBox.

        """
        self.widget = ComboBox()
        self.widget.setImmediate(True)
        parent.addComponent(self.widget)

    def initialize(self):
        """ Intializes the widget with the attributes of this instance.

        """
        super(MuntjacComboBox, self).initialize()
        shell = self.shell_obj
        self.set_items(shell.labels)
        self.set_selection(shell.index)

    def bind(self):
        """ Connects the event handlers for the combo box.

        """
        super(MuntjacComboBox, self).bind()
        self.widget.currentIndexChanged.connect(self.on_selected)

    #--------------------------------------------------------------------------
    # Implementation
    #--------------------------------------------------------------------------
    def shell_index_changed(self, index):
        """ The change handler for the 'index' attribute on the shell
        object.

        """
        self.set_selection(index)

    def shell_labels_changed(self, labels):
        """ The change handler for the 'labels' attribute on the shell
        object.

        """
        self.set_items(labels)

    def on_selected(self):
        """ The event handler for a combo box selection event.

        """
        if not guard.guarded(self, 'updating'):
            shell = self.shell_obj
            curr_index = self._selected_index()
            shell.index = curr_index

            # Only fire the selected event if we have a valid selection
            if curr_index != -1:
                shell.selected = shell.value

    def set_items(self, str_items):
        """ Sets the items in the combo box.

        """
        # We need to avoid a feedback loop when updating the items in
        # the combo box. Qt will emit index changed signals when the
        # items are updated. But, the shell object has already computed
        # the proper index for the new items, so we use that to update
        # the index of the control after updating the items. The flag
        # is read by the on_selected handler to ignore updates during
        # this process.
        with guard(self, 'updating'):
            widget = self.widget
            widget.removeAllItems()
            for item in str_items:
                widget.addItem(item)
            ids = widget.getItemIds()
            widget.select(ids[self.shell_obj.index])

    def set_selection(self, index):
        """ Sets the value in the combo box, or resets the combo box
        if the value is not in the list of items.

        """
        # We need to avoid a feedback loop when updating the selection
        # in the combo box. Qt will emit index changed signals when the
        # selectino is updated. But, the shell object has already computed
        # the proper index for the new selection so we don't need to feed
        # back while doing this.
        with guard(self, 'updating'):
            ids = self.widget.getItemIds()
            self.widget.select(ids[index])

    #--------------------------------------------------------------------------
    # Helper Methods
    #--------------------------------------------------------------------------
    def _selected_index(self):
        widget = self.widget
        ids = widget.getItemIds()
        val = widget.getValue()
        if val in ids:
            curr_index = ids.index(val)
        else:
            curr_index = -1
        return curr_index

