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

from muntjac.api import Label

from .muntjac_control import MuntjacControl

from ..html import AbstractTkHtml


class MuntjacHtml(MuntjacControl, AbstractTkHtml):
    """ A Muntjac implementation of Html.

    """
    #--------------------------------------------------------------------------
    # Setup methods
    #--------------------------------------------------------------------------
    def create(self, parent):
        """ Creates the underlying widget to display HTML.

        """
        self.widget = Label()
        self.widget.setContentMode(Label.CONTENT_XHTML)
        parent.addComponent(self.widget)

    def initialize(self):
        """ Initializes the attributes of the control.

        """
        super(MuntjacHtml, self).initialize()
        self.set_page_source(self.shell_obj.source)

    #--------------------------------------------------------------------------
    # Implementation
    #--------------------------------------------------------------------------
    def shell_source_changed(self, source):
        """ The change handler for the 'source' attribute.

        """
        self.set_page_source(source)

    def set_page_source(self, source):
        """ Sets the page source for the underlying control.

        """
        self.widget.setValue(source)

