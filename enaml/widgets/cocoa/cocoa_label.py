from Foundation import NSMakeRect
from AppKit import NSTextField, NSViewWidthSizable, NSViewHeightSizable


from traits.api import implements

from .cocoa_control import CocoaControl
#from .styling import CocoaStyleHandler, qt_box_model

from ..label import ILabelImpl


class CocoaLabel(CocoaControl):
    """ A Cocoa implementation of Label.

    A CocoaLabel displays static text using a NSTextField control.

    See Also
    --------
    Label

    """
    implements(ILabelImpl)

    #---------------------------------------------------------------------------
    # ILabelImpl interface 
    #---------------------------------------------------------------------------
    def create_widget(self):
        """ Creates the underlying text control.

        """
        self.widget = NSTextField.alloc().init()

    def initialize_widget(self):
        """ Initializes the attributes on the underlying control.

        """
        self.widget.setEditable_(False)
        self.widget.setBordered_(False)
        self.widget.setDrawsBackground_(False)
        self.widget.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)
        self.set_label(self.parent.text)
        

    def parent_text_changed(self, text):
        """ The change handler for the 'text' attribute. Not meant for
        public consumption.

        """
        self.set_label(text)

    #---------------------------------------------------------------------------
    # Widget update
    #---------------------------------------------------------------------------
    def set_label(self, label):
        """ Sets the label on the underlying control. Not meant for
        public consumption.

        """
        self.widget.setStringValue_(label)

    #tags = qt_box_model
