from traits.api import implements

from .cocoa_group import CocoaGroup

from ..vgroup import IVGroupImpl


class CocoaVGroup(CocoaGroup):
    """ A Cocoa implementation of IVGroup.

    This is a convienence subclass of CocoaGroup which restricts the 
    layout direction to vertical.

    See Also
    --------
    IVGroup
    
    """ 
    implements(IVGroupImpl)

    #---------------------------------------------------------------------------
    # IVGroupImpl interface
    #---------------------------------------------------------------------------
    
    # IVGroupImpl interface is empty and fully implemented by CocoaGroup
