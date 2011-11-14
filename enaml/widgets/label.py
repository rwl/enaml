#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from abc import abstractmethod

from traits.api import Str, Instance

from .control import Control, AbstractTkControl


class AbstractTkLabel(AbstractTkControl):
    
    @abstractmethod
    def shell_text_changed(self, text):
        raise NotImplementedError
        
    
class Label(Control):
    """ A simple read-only text display.

    """
    #: The text in the label.
    text = Str
    
    #: How strongly a component hugs it's content.
    #: Labels hug their contents' width weakly.
    hug_width = 'weak'

    #: Overridden parent class trait
    abstract_obj = Instance(AbstractTkLabel)

    def _text_changed(self):
        """ Since the text has changed, the label's size hint has probably
        changed too. The layout system of the parent Container should be
        informed of this.

        """
        self.parent.set_needs_update_constraints(True)
