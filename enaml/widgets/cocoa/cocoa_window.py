from Foundation import NSMakeRect
from AppKit import NSWindow, NSView, \
    NSTitledWindowMask, NSClosableWindowMask, NSMiniaturizableWindowMask, NSResizableWindowMask \
    #NSViewWidthSizeable, NSViewHeightSizable

from traits.api import implements, Instance

from .cocoa_component import CocoaComponent

from ..window import IWindowImpl

from ...enums import Modality

from ...util.guisupport import get_app_cocoa


class CocoaWindow(CocoaComponent):
    """ A Qt implementation of a Window.

    QtWindow uses a QFrame to create a simple top level window which
    contains other child widgets and layouts.

    See Also
    --------
    Window

    """
    implements(IWindowImpl)
    
    _layout = Instance(NSView)

    #---------------------------------------------------------------------------
    # IWindowImpl interface
    #---------------------------------------------------------------------------
    def create_widget(self):
        """ Creates the underlying QWindow control.

        """
        self.widget = NSWindow.alloc().init()
    
    def initialize_widget(self):
        """ Intializes the attributes on the QWindow.

        """
        self.widget.setStyleMask_(NSTitledWindowMask | NSClosableWindowMask | NSMiniaturizableWindowMask |
            NSResizableWindowMask)
        self.set_title(self.parent.title)
        

    def create_style_handler(self):
        """ Creates and sets the window style handler.

        """
        pass
    
    def initialize_style(self):
        """ Initializes the style for the window.

        """
        pass

    def layout_child_widgets(self):
        """ Arranges the children of the QWindow (typically only one) in
        a vertical box layout.

        """
        self._layout = NSView.alloc().init()
        #self._layout.setAutoresizingMask_(NSViewWidthSizeable | NSViewHeightSizable)
        for child in self.child_widgets():
            self._layout.addSubview_(child)
        self.widget.setContentView_(self._layout)

    def show(self):
        """ Displays the window to the screen.
        
        """
        if self.widget:
            modality = self.parent.modality
            if modality == Modality.APPLICATION_MODAL or modality == Modality.WINDOW_MODAL:
                self.start_modal()
            self.widget.makeKeyAndOrderFront_(None)

    def hide(self):
        """ Hide the window from the screen.

        """
        if self.widget:
            modality = self.parent.modality
            if modality == Modality.APPLICATION_MODAL or modality == Modality.WINDOW_MODAL:
                self.stop_modal()
            self.widget.orderOut_()

    def parent_title_changed(self, title):
        """ The change handler for the 'title' attribute. Not meant for 
        public consumption.

        """
        self.set_title(title)
    
    def parent_modality_changed(self, modality):
        """ The change handler for the 'modality' attribute. Not meant 
        for public consumption.

        """
        if modality == Modality.APPLICATION_MODAL or modality == Modality.WINDOW_MODAL:
            self.start_modal()
        else:
            self.stop_modal()

    #---------------------------------------------------------------------------
    # Implementation
    #---------------------------------------------------------------------------
    def set_title(self, title):
        """ Sets the title of the QFrame. Not meant for public 
        consumption.

        """
        if self.widget:
            self.widget.setTitle_(title)
    
    def start_modal(self):
        """ Puts the application into Modal state using this window.
        
        Not meant for public consumption.
        """
        if self.widget:
            app = self.cocoa_get_app()
            app.runModalForWindow_(self.widget)
            
    def stop_modal(self):
        """ If the application was in Modal state, this clears it.
        
        Not meant for public consumption.
        """
        if self.widget:
            app = self.cocoa_get_app()
            app.stopModal()
