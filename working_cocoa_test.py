""" A working example that tracks the development of the widgets
on the pyside branch and can be executed via python working_pyside_test.py 
from the current directory.

"""
from cStringIO import StringIO
import random

from traits.api import HasTraits, Str

from enaml.factory import EnamlFactory
from enaml.toolkit import cocoa_toolkit

enml = """
import math
import random
import datetime

from enaml.enums import Direction

Window:
    pass
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


fact = EnamlFactory(StringIO(enml), toolkit=cocoa_toolkit())

view = fact(model=Model())

view.show()


