#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------

import enaml
from enaml.parsing.builders import enaml_defn, make_widget, \
    simple, delegate, bind, notify



@enaml_defn
def MainWindow():
    
    Window = make_widget('Window')
    Label = make_widget('Label')
    Field = make_widget('Field')
    
    return Window(
        delegate('title', "field.value"),
        simple('constraints', """[
            vertical(top, frame, bottom),
            vertical(top, field, bottom),
            horizontal(left, frame, field, right),
        ]"""),
        Label('frame',
            simple('text', '"Title:"'),
        ),
        Field('field',
            simple('value', "'It Works!'"),
        )
    )

print repr(MainWindow)

if __name__ == '__main__':
    view = MainWindow()
    view.show()