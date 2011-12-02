#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------

from traits.api import HasTraits, Str, CInt, Password, Property, cached_property
from enaml.traits_view import configure_traits, bind, TView, TForm, TItem

class Person(HasTraits):
    first_name = Str
    last_name = Str
    age = CInt(enaml_control='ErrorField')
    password = Password
    
    full_name = Property(Str, depends_on=['first_name', 'last_name'], binding=bind)
    
    @cached_property
    def _get_full_name(self):
        return self.first_name + ' ' + self.last_name

if __name__ == '__main__':
    person = Person(first_name='John', last_name='Citizen')
    #view = TraitsView(Form('first_name', 'last_name', 'full_name', 'age', 'password'))
    view=None
    configure_traits(person, view)
