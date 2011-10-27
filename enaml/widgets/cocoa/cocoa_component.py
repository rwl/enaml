from .cocoa_base_component import CocoaBaseComponent

from ..component import AbstractTkComponent

from Foundation import NSMakeRect
from AppKit import NSView, NSViewWidthSizable, NSViewHeightSizable


class CocoaComponent(CocoaBaseComponent, AbstractTkComponent):
    """ A Cocoa implementation of Component.

    A CocoaComponent is not meant to be used directly. It provides some 
    common functionality that is useful to all widgets and should 
    serve as the base class for all other classes. Note that this 
    is not a HasTraits class.
    """
    #: The Cocoa widget created by the component
    widget = None

    #--------------------------------------------------------------------------
    # Setup Methods
    #--------------------------------------------------------------------------
    def create(self):
        self.widget = NSView.alloc().init()
        self._view = self.widget
    
    def initialize(self):
        for child in self.child_widgets():
            self._view.addSubview_(child)
    
    def bind(self):
        super(CocoaComponent, self).bind()
        
        # This is a hack at the moment
        if hasattr(self.widget, 'resized'):
            self.widget.resized.connect(self.on_resize)

    #--------------------------------------------------------------------------
    # Implementation
    #--------------------------------------------------------------------------
    @property
    def toolkit_widget(self):
        """ A property that returns the toolkit specific widget for this
        component.

        """
        return self.widget
    
    def size(self):
        """ Return the size of the internal toolkit widget as a 
        (width, height) tuple of integers.

        """
        width, height = self.widget.Frame.size
        return (width, height)
    
    def size_hint(self):
        """ Returns a (width, height) tuple of integers which represent
        the suggested size of the widget for its current state. This 
        value is used by the layout manager to determine how much 
        space to allocate the widget.

        """
        return (400, 400)

    def resize(self, width, height):
        """ Resizes the internal toolkit widget according the given
        width and height integers.

        """
        self.widget.setFrameSize_(width, height)
    
    def pos(self):
        """ Returns the position of the internal toolkit widget as an 
        (x, y) tuple of integers. The coordinates should be relative to
        the origin of the widget's parent.

        """
        return self.geometry()[:2]
    
    def move(self, x, y):
        """ Moves the internal toolkit widget according to the given
        x and y integers which are relative to the origin of the
        widget's parent.

        """
        super_w, super_h = self.widget.superview.Frame.size
        width, height = self.widget.Frame.size
        self.widget.setFrameOrigin_(x, super_h-y-height)
    
    def geometry(self):
        """ Returns an (x, y, width, height) tuple of geometry info
        for the internal toolkit widget. The semantic meaning of the
        values are the same as for the 'size' and 'pos' methods.

        """
        (x, y), (width, height) = self.widget.Frame
        super_w, super_h = self.widget.superview.Frame.size
        return (x, super_h-y-height, width, height)
    
    def set_geometry(self, x, y, width, height):
        """ Sets the geometry of the internal widget to the given 
        x, y, width, and height values. The semantic meaning of the
        values is the same as for the 'resize' and 'move' methods.

        """
        print 'setting geometry'
        super_w, super_h = self.widget.superview.Frame.size
        self.widget.setFrame_(NSMakeRect(x, super_h-y-height, width, height))
    
    def on_resize(self):
        # should handle the widget resizing by telling something
        # that things need to be relayed out
        pass

    #--------------------------------------------------------------------------
    # Convienence methods
    #--------------------------------------------------------------------------
    def parent_widget(self):
        """ Returns the logical NSResponder parent for this component. 

        Since some parents may wrap non-Widget objects, this method will
        walk up the tree of components until a NSResponder is found or None 
        if no NSResponder is found.

        Returns
        -------
        result : NSResponder or None

        """
        # XXX do we need to do this still? i.e. can we now have a parent
        # that doesn't create a widget???
        shell_parent = self.shell_obj.parent
        while shell_parent:
            widget = shell_parent.toolkit_widget
            if isinstance(widget, NSResponder):
                return widget
            shell_parent = shell_parent.parent
        
    def child_widgets(self):
        """ Iterates over the shell widget's children and yields the 
        toolkit widgets for those children.

        """
        for child in self.shell_obj.children:
            yield child.toolkit_widget

