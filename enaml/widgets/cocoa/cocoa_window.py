from Foundation import NSMakeRect
from AppKit import NSWindow, NSView, \
    NSTitledWindowMask, NSClosableWindowMask, NSMiniaturizableWindowMask, NSResizableWindowMask, \
    NSViewWidthSizable, NSViewHeightSizable

from traits.api import implements, Instance

from .cocoa_component import CocoaComponent

from ..window import AbstractTkWindow

from ...enums import Modality

from ...util.guisupport import get_app_cocoa


class CocoaWindow(CocoaComponent, AbstractTkWindow):
    """ A Cocoa implementation of a Window.

    CocoaWindow uses a QFrame to create a simple top level window which
    contains other child widgets and layouts.

    See Also
    --------
    Window

    """
    #--------------------------------------------------------------------------
    # Setup methods
    #--------------------------------------------------------------------------
    def create(self):
        """ Creates the underlying QWindow control.

        """
        self.widget = NSWindow.alloc().init()
        self.widget.setFrame_display_(NSMakeRect(100,100,200,250), False)
        self._view = NSView.alloc().init()
    
    def initialize(self):
        """ Intializes the attributes on the QWindow.

        """
        super(CocoaWindow, self).initialize()

        self._view.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)
        self.widget.setContentView_(self._view)

        self.widget.setStyleMask_(NSTitledWindowMask | NSClosableWindowMask | NSMiniaturizableWindowMask |
            NSResizableWindowMask)
        shell = self.shell_obj
        self.set_title(shell.title)
        if shell.modality == Modality.APPLICATION_MODAL or shell.modality == Modality.WINDOW_MODAL:
            self.start_modal()
        else:
            self.stop_modal()

    #--------------------------------------------------------------------------
    # Implementation
    #--------------------------------------------------------------------------
    def show(self):
        """ Displays the window to the screen.
        
        """
        if self.widget:
            shell = self.shell_obj
            modality = shell.modality
            if modality == Modality.APPLICATION_MODAL or modality == Modality.WINDOW_MODAL:
                self.start_modal()
            self.widget.makeKeyAndOrderFront_(None)
            self.widget.display()

    def hide(self):
        """ Hide the window from the screen.

        """
        if self.widget:
            shell = self.shell_obj
            modality = shell.modality
            if modality == Modality.APPLICATION_MODAL or modality == Modality.WINDOW_MODAL:
                self.stop_modal()
            self.widget.orderOut_()

    def shell_title_changed(self, title):
        """ The change handler for the 'title' attribute. Not meant for 
        public consumption.

        """
        self.set_title(title)
    
    def shell_modality_changed(self, modality):
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
            app = get_app_cocoa()
            app.runModalForWindow_(self.widget)
            
    def stop_modal(self):
        """ If the application was in Modal state, this clears it.
        
        Not meant for public consumption.
        """
        if self.widget:
            app = get_app_cocoa()
            app.stopModal()
