#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------

from traits.api import HasTraits, Str, Any, Dict, List, Either, Instance, Property, cached_property
from traits.trait_handlers import _read_only, _write_only, _undefined_get, _undefined_set

import enaml
with enaml.imports():
    from enaml.stdlib.fields import *

from .parsing.builders import EnamlPyCall, simple, bind, delegate, notify, enaml_defn, make_widget

_widget_factories = {}

class TraitControlRegistry(HasTraits):
    
    registry = Dict
    
    widget_factories = Dict
    
    def get_control(self, trait, name):
        """ Return an appropriate Enaml control for a given CTrait.
        
        """
        # check 'enaml_control' metadata
        control = trait.enaml_control
        
        # otherwise search mro for something in the registry
        if control is None:
            for trait_type in trait.trait_type.__class__.mro():
                if trait_type in self.registry:
                    control = self.registry[trait_type]
                    break
            else:
                control = 'ReadOnlyField'
        
        if isinstance(control, basestring):
            if control not in self.widget_factories:
                self.widget_factories[control] = make_widget(control)
            control = self.widget_factories[control]
        elif callable(control):
            control = control(trait, name)
        
        return control
 
                
    def _registry_default(self):
        """ A default set of choices for Controls to use with different trait types
        
        """
        from traits.api import (BaseBool, BaseInt, BaseLong, BaseFloat,
                BaseComplex, BaseStr, BaseUnicode, String, Code, HTML, Password)
        return {
            BaseBool: 'CheckBox',
            BaseInt: 'IntField',
            BaseLong: 'LongField',    
            BaseFloat: 'FloatField',
            BaseComplex: 'ComplexField',
            BaseStr: 'ErrorField',
            BaseUnicode: 'ErrorField',
            String: 'ErrorField',
            Code: 'CodeEditor',
            HTML: 'Html',
            Password: 'PasswordField',
        }

default_registry = TraitControlRegistry()

class TraitsItem(HasTraits):
    control = Any
    binding = Any(delegate)
    name = Str
    label = Str
    label_class = Any
    registry = Instance(TraitControlRegistry)

    def build(self, model):
        print self.name
        trait = model.traits()[self.name]
        label = self.label_class(simple('text', repr(self.label)))
        binding = self.binding
        control = self.get_control(trait)(
            self.binding('value', 'model.'+self.name),
            simple('read_only', str(not self.isWriteable(trait))),
        )
        return [label, control]

    def get_control(self, trait):
        if self.control is not None:
            return self.control
        else:
            return self.registry.get_control(trait, self.name)
    
    def isWriteable(self, trait):
        """ Utility method to determine whether trait is writeable
        """
        if trait.type == 'property':
            getter, setter, validate = trait.property()
            return setter != _read_only and setter != _undefined_set
        elif trait.type == 'constant':
            return False
        
        return True

        
    def isReadable(self, trait):
        """ Utility method to determine whether trait is readable
        """
        if trait.type == 'property':
            getter, setter, validate = trait.property()
            return getter != _write_only and setter != _undefined_get
        elif trait.type == 'constant':
            return False
        
        return True
    
    def _label_default(self):
        return self.name.replace('_', ' ').capitalize()+':'
    
    def _label_class_default(self):
        return make_widget('Label')
    
    def _registry_default(self):
        return default_registry


class TraitsGroup(HasTraits):
    container_class = Str("Form")
    
    container = Property(Any, depends_on='container_class')
    
    items = List(Either(TraitsItem, 'TraitsGroup'))
    
    def build(self, model):
        contents = sum((item.build(model) for item in self.items), [])
        return [
            self.container(
                *contents
            )
        ]
    
    @cached_property
    def _get_container(self):
        return _widget_factories.setdefault(self.container_class,
                make_widget(self.container_class))
        
class TraitsView(HasTraits):
    window_class = Str("Window")
    
    window = Property(Any, depends_on='window_class')

    items = List(Either(TraitsItem, TraitsGroup))

    def build(self, model):
        if not self.items:
            self.default_layout(model)
        else:
            contents = sum((item.build(model) for item in self.items), [])
        return self.window(
            *contents
        )
    
    
    def default_layout(self, model):
        items = [TraitsItem(name=trait) for trait in sorted(model.trait_names())
                if trait != 'trait_added' and trait != 'trait_modified']
        form = TraitsGroup(*items)
        rteurn [form]
    
    @cached_property
    def _get_window(self):
        return _widget_factories.setdefault(self.window_class,
                make_widget(self.window_class))

@enaml_defn
def build(model, view=None):
    if view is None:
        items = [TraitsItem(name=trait) for trait in sorted(model.trait_names())
                if trait[0] != '_' and trait != 'trait_added' and trait != 'trait_modified']
        form = TraitsGroup(items=items)
        view = TraitsView(items=[form])
    return view.build(model)
    
    
def edit_traits(model, view=None):
    view = build(model, view)
    view.show(start_app=False)
    return view
    
def configure_traits(model, view=None):
    view = build(model, view)
    view.show()
