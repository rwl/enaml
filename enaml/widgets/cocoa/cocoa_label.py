from Foundation import NSMakeRect
from AppKit import NSTextField, NSViewWidthSizable, NSViewHeightSizable

from .cocoa_control import CocoaControl

from ..label import AbstractTkLabel


class CocoaLabel(CocoaControl, AbstractTkLabel):
    """ A Cocoa implementation of Label.

    A CocoaLabel displays static text using a NSTextField control.
    """
    #--------------------------------------------------------------------------
    # Setup methods
    #--------------------------------------------------------------------------
    def create(self):
        """ Creates the underlying text control.

        """
        print 'creating label'
        self.widget = NSTextField.alloc().init()

    def initialize(self):
        """ Initializes the attributes on the underlying control.

        """
        print 'initializing label'
        super(CocoaLabel, self).initialize()
        self.widget.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)
        
        self.widget.setEditable_(False)
        self.widget.setBordered_(False)
        self.widget.setDrawsBackground_(False)
        
        self.set_label(self.shell_obj.text)
    
    def size_hint(self):
        """ Returns a (width, height) tuple of integers which represent
        the suggested size of the widget for its current state. This 
        value is used by the layout manager to determine how much 
        space to allocate the widget.

        """
        return (100, 100)

    #--------------------------------------------------------------------------
    # Implementation
    #--------------------------------------------------------------------------
    def shell_text_changed(self, text):
        """ The change handler for the 'text' attribute. Not meant for
        public consumption.

        """
        self.set_label(text)
        # XXX we might need a relayout call here when the text changes
        # since it's width may have changed and the size hint may 
        # now be different. We probably want to make it configurable
        # though since fixed width labels don't need a relayout

    def set_label(self, label):
        """ Sets the label on the underlying control. Not meant for
        public consumption.

        """
        self.widget.setStringValue_(label)
