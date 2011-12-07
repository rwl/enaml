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

from muntjac.api import Table

from .muntjac_control import MuntjacControl
from .abstract_item_model_wrapper import AbstractItemModelWrapper

from ..table_view import AbstractTkTableView


class MuntjacTableView(MuntjacControl, AbstractTkTableView):
    """ A Muntjac implementation of TableView.

    See Also
    --------
    TableView

    """
    #: The underlying model.
    model_wrapper = None

    #--------------------------------------------------------------------------
    # Setup methods
    #--------------------------------------------------------------------------
    def create(self, parent):
        """ Create the underlying Table control.

        """
        self.widget = Table()
        parent.addComponent(self.widget)

    def initialize(self):
        """ Initialize the widget with the attributes of this instance.

        """
        super(MuntjacTableView, self).initialize()
        shell = self.shell_obj
        self.set_table_model(shell.item_model)
        self.set_vertical_header_vis(shell.vertical_header_visible)
        self.set_horizontal_header_vis(shell.horizontal_header_visible)

    #--------------------------------------------------------------------------
    # Implementation
    #--------------------------------------------------------------------------
    def shell_item_model_changed(self, item_model):
        """ The change handler for the 'item_model' attribute.

        """
        self.set_table_model(item_model)

    def shell_vertical_header_visible_changed(self, visible):
        self.set_vertical_header_vis(visible)

    def shell_horizontal_header_visible_changed(self, visible):
        self.set_horizontal_header_vis(visible)

    def set_table_model(self, model):
        """ Set the table view's model.

        """
        model_wrapper = AbstractItemModelWrapper(model)
        self.widget.setContainerDataSource(model_wrapper)
        self.model_wrapper = model_wrapper

    def set_vertical_header_vis(self, visible):
        if visible:
            self.widget.setRowHeaderMode(Table.ROW_HEADER_MODE_EXPLICIT)
        else:
            self.widget.setRowHeaderMode(Table.ROW_HEADER_MODE_HIDDEN)

    def set_horizontal_header_vis(self, visible):
        if visible:
            self.widget.setColumnHeaderMode(Table.COLUMN_HEADER_MODE_EXPLICIT)
        else:
            self.widget.setColumnHeaderMode(Table.COLUMN_HEADER_MODE_HIDDEN)

