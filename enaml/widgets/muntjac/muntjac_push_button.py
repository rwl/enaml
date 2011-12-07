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

from muntjac.api import Button

from .muntjac_control import MuntjacControl

from ..push_button import AbstractTkPushButton


class MuntjacPushButton(MuntjacControl, AbstractTkPushButton):
    """ A Muntjac implementation of PushButton.

    """
    #--------------------------------------------------------------------------
    # Setup methods
    #--------------------------------------------------------------------------
    def create(self, parent):
        """ Creates the underlying Button control.

        """
        self.widget = Button()
        self.widget.setImmediate(True)
        parent.addComponent(self.widget)

    def initialize(self):
        """ Intializes the widget with the attributes of this instance.

        """
        super(MuntjacPushButton, self).initialize()
        self.set_label(self.shell_obj.text)

    def bind(self):
        """ Connects the event handlers for the push button.

        """
        super(MuntjacPushButton, self).bind()
        widget = self.widget
        widget.clicked.connect(self.on_clicked)
        widget.pressed.connect(self.on_pressed)
        widget.released.connect(self.on_released)

    #--------------------------------------------------------------------------
    # Implementation
    #--------------------------------------------------------------------------
    def shell_text_changed(self, text):
        """ The change handler for the 'text' attribute.

        """
        self.set_label(text)
        # If the text of the button changes, the size hint has likely
        # change and the layout system needs to be informed.
        self.shell_obj.size_hint_updated = True

    def on_clicked(self):
        """ The event handler for the button's clicked event.

        """
        shell = self.shell_obj
        shell._down = False
        shell.clicked = True

    def on_pressed(self):
        """ The event handlers for the button's pressed event.

        """
        shell = self.shell_obj
        shell._down = True
        shell.pressed = True

    def on_released(self):
        """ The event handler for the button's released event.

        """
        shell = self.shell_obj
        if shell._down:
            shell._down = False
            shell.released = True

    def set_label(self, label):
        """ Sets the label on the button control.

        """
        self.widget.setCaption(label)

