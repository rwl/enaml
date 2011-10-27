import weakref

from ..base_component import AbstractTkBaseComponent

class CocoaBaseComponent(AbstractTkBaseComponent):
    _shell_obj = lambda: None

    def _get_shell_obj(self):
        """ Returns a strong reference to the shell object.

        """
        return self._shell_obj()
    
    def _set_shell_obj(self, obj):
        """ Stores a weak reference to the shell object.

        """
        self._shell_obj = weakref.ref(obj)
    
    #: A property which gets a sets a reference (stored weakly)
    #: to the shell object
    shell_obj = property(_get_shell_obj, _set_shell_obj)

    def create(self):
        """ Create the underlying toolkit object. 

        This method is called after the reference to the shell object
        has been set and is called in depth-first order. This means
        that by the time this method is called, the logical parent
        of this instance has already been created. This method
        must be implemented by subclasses.

        """
        raise NotImplementedError
    
    def initialize(self):
        """ Initialize the toolkit object.

        This method is called after 'create' in depth-first order. This
        means that all other implementations in the tree will have been
        created so that intialization can depend on the existence of 
        other implementation objects. Subclasses may optionally 
        implement this method.

        """
        pass
    
    def bind(self):
        """ Called after 'initialize' in order to bind event handlers.

        At the time this method is called, the entire tree of ui
        objects will have been initialized. The intention of this 
        method is delay the binding of event handlers until after
        everything has been intialized in order to mitigate extraneous
        event firing. Subclasses may optionally implement this method.

        """
        pass


#     """ A Cocoa implementation of BaseComponent.
# 
#     A CocoaBaseComponent is not meant to be used directly. It provides some 
#     common functionality that is useful to all widgets and should 
#     serve as the base class for all other classes.
# 
#     See Also
#     --------
#     BaseComponent
# 
#     """
# 
#     #---------------------------------------------------------------------------
#     # IComponentImpl interface
#     #---------------------------------------------------------------------------
#     shell_obk = WeakRef(Component)
# 
#     def set_parent(self, parent):
#         """ Sets the parent component to the given parent.
# 
#         """
#         self.parent = parent
#         
#     def create_widget(self):
#         """ Creates the underlying wx widget. Must be implemented by 
#         subclasses.
# 
#         """
#         raise NotImplementedError
#     
#     def initialize_widget(self):
#         """ Initializes the attribtues of a wiget. Must be implemented
#         by subclasses.
# 
#         """
#         raise NotImplementedError
#     
#     def create_style_handler(self):
#         """ Creates and sets the style handler for the widget. Must
#         be implemented by subclasses.
# 
#         """
#         raise NotImplementedError
# 
#     def initialize_style(self):
#         """ Initializes the style and style handler of a widget. Must
#         be implemented by subclasses.
# 
#         """
#         raise NotImplementedError
# 
#     def layout_child_widgets(self):
#         """ Arranges the children of this component. Must be implemented
#         by subclasses.
# 
#         """
#         raise NotImplementedError
#     
#     def toolkit_widget(self):
#         """ Returns the toolkit specific widget for this component.
# 
#         """
#         return self.widget
#     
#     def parent_name_changed(self, name):
#         """ The change handler for the 'name' attribute on the parent.
#         QtComponent doesn't care about the name. Subclasses should
#         reimplement if they need that info.
# 
#         """
#         pass    
# 
#     #---------------------------------------------------------------------------
#     # Implementation
#     #---------------------------------------------------------------------------
#     widget = Instance(NSObject)
#         
#     def parent_widget(self):
#         """ Returns the logical QWidget parent for this component. 
# 
#         Since some parents may wrap non-Widget objects, this method will
#         walk up the tree of parent components until a QWindow is found
#         or None if no QWindow is found.
# 
#         Arguments
#         ---------
#         None
# 
#         Returns
#         -------
#         result : QWidget or None
# 
#         """
#         # Our parent is a Component, and the parent of 
#         # a Component is also a Component
#         parent = self.parent
#         while parent:
#             widget = parent.toolkit_widget()
#             return widget
#             #if isinstance(widget, QtGui.QWidget):
#             #    return widget
#             #parent = parent.parent
#         
#     def child_widgets(self):
#         """ Iterates over the parent's children and yields the 
#         toolkit widgets for those children.
# 
#         """
#         for child in self.parent.children:
#             yield child.toolkit_widget()
# 
#     #---------------------------------------------------------------------------
#     # Implementation
#     #---------------------------------------------------------------------------
