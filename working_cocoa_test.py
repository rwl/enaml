""" A working example that tracks the development of the widgets
on the pyside branch and can be executed via python working_pyside_test.py 
from the current directory.

"""
from cStringIO import StringIO
import random

from traits.api import HasTraits, Str

import enaml

with enaml.imports():
    from working_cocoa_test import MainWindow


rest = """
    Panel:
        Group:
            Label:
                text = model.message
            Label:
                text = "More text"
"""

class Model(HasTraits):

    message = Str('Foo Model Message!')

    window_title = Str('Window Title!')

    def print_msg(self, args):
        print self.message, args

    def randomize(self, string):
        l = list(string)
        random.shuffle(l)
        return ''.join(l)


view = MainWindow(model=Model())
view.show()


