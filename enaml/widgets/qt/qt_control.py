from traits.api import implements

from .qt_component import QtComponent

from ..control import IControlImpl


class QtControl(QtComponent):

    implements(IControlImpl)

    #---------------------------------------------------------------------------
    # IControlImpl interface
    #---------------------------------------------------------------------------
    def layout_child_widgets(self):
        """ Ensures that the control does not contain children. Special
        control subclasses that do allow for children should reimplement
        this method.

        """
        if list(self.child_widgets()):
            raise ValueError('Standard controls cannot have children.')
