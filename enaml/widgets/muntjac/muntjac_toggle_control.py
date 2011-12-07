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

from ..toggle_control import AbstractTkToggleControl


class MuntjacToggleControl(MuntjacControl, AbstractTkToggleControl):
    """ A base class for Muntjac toggle widgets.

    This class can serve as a base class for widgets that implement
    toggle behavior such as CheckBox and RadioButton. It is not meant
    to be used directly. Subclasses should implement the 'create'
    and bind methods.

    Furthermore, the toggled, pressed and released event that is generated
    by the toolkit widget needs to be bound to the on_toggled(),
    on_pressed() and on_released() methods.

    """
    #--------------------------------------------------------------------------
    # Setup methods
    #--------------------------------------------------------------------------
    def initialize(self):
        """ Initializes the attributes of the underlying control.

        """
        super(MuntjacToggleControl, self).initialize()
        shell = self.shell_obj
        self.set_label(shell.text)
        self.set_checked(shell.checked)

    #--------------------------------------------------------------------------
    # Implementation
    #--------------------------------------------------------------------------
    def shell_checked_changed(self, checked):
        """ The change handler for the 'checked' attribute.

        """
        self.set_checked(checked)

    def shell_text_changed(self, text):
        """ The change handler for the 'text' attribute.

        """
        self.set_label(text)
        # If the label of the control changes, its size hint has likely
        # updated and the layout system needs to be informed
        self.shell_obj.size_hint_updated = True

    def on_toggled(self):
        """ The event handler for the toggled event.

        """
        shell = self.shell_obj
        shell.checked = self.widget.getValue()
        shell.toggled = True

    def on_pressed(self):
        """ The event handler for the pressed event. Not meant for
        public consumption.

        """
        shell = self.shell_obj
        shell._down = True
        shell.pressed = True

    def on_released(self):
        """ The event handler for the released event. Not meant for
        public consumption.

        """
        shell = self.shell_obj
        if shell._down:
            shell._down = False
            shell.released = True

    def set_label(self, label):
        """ Sets the widget's label with the provided value. Not
        meant for public consumption.

        """
        self.widget.setCaption(label)

    def set_checked(self, checked):
        """ Sets the widget's checked state with the provided value.
        Not meant for public consumption.

        """
        self.widget.setValue(checked)

