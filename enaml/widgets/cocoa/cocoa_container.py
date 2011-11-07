from .cocoa_component import CocoaComponent

from ..container import AbstractTkContainer


class CocoaContainer(CocoaComponent, AbstractTkContainer):
    """ A Cocoa implementation of Container.

    CocoaContainer is usually to be used as a base class for other container
    widgets. However, it may also be used directly as an undecorated container
    for widgets for layout purposes.

    """

    # The CocoaComponent implementation is enough.
    pass
