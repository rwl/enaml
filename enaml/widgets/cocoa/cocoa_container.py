from traits.api import implements

from .cocoa_component import CocoaComponent

from ..container import IContainerImpl


class CocoaContainer(CocoaComponent):
    """ A Cocoa implementation of Container.

    The CocoaContainer class serves as a base class for other container
    widgets. It is not meant to be used directly.

    See Also
    --------
    Container

    """
    implements(IContainerImpl)

    #---------------------------------------------------------------------------
    # IContainerImpl interface
    #---------------------------------------------------------------------------
    def create_style_handler(self):
        """ Creates and sets the window style handler.

        """
        pass
    
    def initialize_style(self):
        """ Initializes the style for the window.

        """
        pass
