#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------

import enaml
from enaml.parsing.builders import EnamlPyDefn, EnamlPyWidget, \
    Default, Delegate, Bind, Notify, compile_defn

class Window(EnamlPyWidget):
    pass

class Label(EnamlPyWidget):
    pass

class Field(EnamlPyWidget):
    pass

def build_defn():
    pydefn = EnamlPyDefn('MainWindow',
        Window(
            Delegate('title', "field.value"),
            Default('constraints', """[
                vertical(top, frame, bottom),
                vertical(top, field, bottom),
                horizontal(left, frame, field, right),
            ]"""),
            Label(
                Default('text', '"Title:"'),
                unpack=['frame']
            ),
            Field(
                Default('value', "'It Works!'"),
                unpack=['field'],
            )
        )
    )
    defn_ast = pydefn.ast()
    return compile_defn(defn_ast, {})

if __name__ == '__main__':
    defn = build_defn()
    print defn.__name__
    print defn.__code__
    print defn.__globals__.keys()

    view = defn()
    view.show()