#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------

from traits.api import HasTraits, Str, CInt, Range, Password, Enum, List, Property, cached_property
from enaml.traits_view import configure_traits, bind, TView, TForm, TItem, TVSplit

class Person(HasTraits):
    first_name = Str
    last_name = Str
    gender = Enum(values='genders')
    genders = List(Str, ['Female', 'Male'])
    #age = CInt(enaml_control='ErrorField')
    age = Range(1,500)
    password = Password
    
    full_name = Property(Str, depends_on=['first_name', 'last_name'], binding=bind)
    
    @cached_property
    def _get_full_name(self):
        return self.first_name + ' ' + self.last_name

if __name__ == '__main__':
    person = Person(first_name='John', last_name='Citizen', gender='Male')
    view = TView(TVSplit(
        TForm('first_name', 'last_name', 'full_name'),
        TForm('gender', 'age', 'password')
    ))
    #view=None
    configure_traits(person, view)
