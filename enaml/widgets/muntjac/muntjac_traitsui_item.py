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

from .muntjac_control import MuntjacControl

from ..traitsui_item import AbstractTkTraitsUIItem


class MuntjacTraitsUIItem(MuntjacControl, AbstractTkTraitsUIItem):
    """ A Muntjac implementation of TraitsUIItem.

    The traits ui item allows the embedding of a traits ui window in
    an Enaml application.

    See Also
    --------
    TraitsUIItem

    """
    ui = None

    #--------------------------------------------------------------------------
    # Setup methods
    #--------------------------------------------------------------------------
    def create(self, parent):
        """ Creates the underlying traits ui subpanel.

        """
        shell = self.shell_obj
        model = shell.model
        view = shell.view
        handler = shell.handler
        self.ui = ui = model.edit_traits(parent=parent, view=view,
                                         handler=handler, kind='subpanel')
        self.widget = ui.control

    #--------------------------------------------------------------------------
    # Implementation
    #--------------------------------------------------------------------------
    def shell_model_changed(self, model):
        raise NotImplementedError

    def shell_view_changed(self, view):
        raise NotImplementedError

    def shell_handler_changed(self, handler):
        raise NotImplementedError

