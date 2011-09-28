from Foundation import NSMakeRect
from AppKit import NSView

from traits.api import implements

from .cocoa_container import CocoaContainer

from ..group import IGroupImpl

from ...enums import Direction


class CocoaGroup(CocoaContainer):
    """ A Cocoa implementation of IGroup.

    The CocoaGroup uses a NSView to arrange its child components.

    See Also
    --------
    IGroup

    """
    implements(IGroupImpl)

    #---------------------------------------------------------------------------
    # IGroupImpl interface
    #---------------------------------------------------------------------------
    def create_widget(self):
        """ Creates the underlying sizer for the group. 

        """
        self.widget = self.make_layout(self.parent.direction)
        
    def initialize_widget(self):
        """ Nothing to initialize on a group.

        """
        pass

    def layout_child_widgets(self):
        """ Adds the children of this container to the sizer.

        """
        layout = self.widget
        for child in self.child_widgets():
            layout.addSubview_(child)

    def parent_direction_changed(self, direction):
        """ The change handler for the 'direction' attribute on the 
        parent.

        """
        pass
    
    #---------------------------------------------------------------------------
    # Implementation
    #---------------------------------------------------------------------------
    def convert_direction(self, direction):
        """ Translate an Enaml Direction constant to a QBoxLayout Direction
        constant.
        """
        return _QBoxLayoutDirections.get(direction, CocoaGui.QBoxLayout.LeftToRight)
    
    def make_layout(self, direction):
        """ Creates a NSView for the given direction value. Not
        meant for public consumption.

        """
        layout = NSView.alloc().init()
        return layout
        
    def set_direction(self, direction):
        self.widget.setDirection(self.convert_direction(direction))
        
    def is_reverse_direction(self, direction):
        """ Returns True or False depending on if the given direction
        is reversed from normal. Not meant for public consumption.

        """
        dirs = (Direction.RIGHT_TO_LEFT, Direction.BOTTOM_TO_TOP)
        return direction in dirs

