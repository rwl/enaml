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

import weakref

from ..base_component import AbstractTkBaseComponent


class MuntjacBaseComponent(AbstractTkBaseComponent):
    """ Base component object for the Muntjac based backend.

    """
    _shell_obj = lambda: None

    def _get_shell_obj(self):
        """ Returns a strong reference to the shell object.

        """
        return self._shell_obj()

    def _set_shell_obj(self, obj):
        """ Stores a weak reference to the shell object.

        """
        self._shell_obj = weakref.ref(obj)

    #: A property which gets a sets a reference (stored weakly)
    #: to the shell object
    shell_obj = property(_get_shell_obj, _set_shell_obj)

    def create(self, parent):
        """ Create the underlying toolkit object.

        This method is called after the reference to the shell object
        has been set and is called in depth-first order. This means
        that by the time this method is called, the logical parent
        of this instance has already been created. This method
        must be implemented by subclasses.

        """
        raise NotImplementedError

    def initialize(self):
        """ Initialize the toolkit object.

        This method is called after 'create' in depth-first order. This
        means that all other implementations in the tree will have been
        created so that intialization can depend on the existence of
        other implementation objects. Subclasses may optionally
        implement this method.

        """
        pass

    def bind(self):
        """ Called after 'initialize' in order to bind event handlers.

        At the time this method is called, the entire tree of ui
        objects will have been initialized. The intention of this
        method is delay the binding of event handlers until after
        everything has been intialized in order to mitigate extraneous
        event firing. Subclasses may optionally implement this method.

        """
        pass

    def shell_enabled_changed(self, enabled):
        """ The change handler for the 'enabled' attribute on the shell
        object. Should be implemented by subclasses where appropriate.

        """
        pass

    def shell_visible_changed(self, visible):
        """ The change handler for the 'visible' attribute on the shell
        object. Should be implemented by subclasses where appropriate.

        """
        pass

    def shell_bg_color_changed(self, color):
        """ The change handler for the 'bg_color' attribute on the shell
        object. Should be implemented by subclasses where appropriate.

        """
        pass

    def shell_fg_color_changed(self, color):
        """ The change handler for the 'fg_color' attribute on the shell
        object. Should be implemented by subclasses where appropriate.

        """
        pass

    def shell_font_changed(self, font):
        """ The change handler for the 'font' attribute on the shell
        object. Should be implemented by subclasses where appropriate.

        """
        pass

