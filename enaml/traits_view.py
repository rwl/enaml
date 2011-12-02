#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from types import CodeType

from traits.api import HasTraits, Str, Any, Dict, List, Either, Instance, Property, cached_property
from traits.trait_handlers import _read_only, _write_only, _undefined_get, _undefined_set

import enaml
with enaml.imports():
    from enaml.stdlib.fields import *
    from enaml.stdlib.containers import *

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
                BaseComplex, BaseStr, BaseUnicode, String, Code, HTML, Password,
                Range, Enum,)
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
            Enum: TEnumEditor,
            Range: TRangeEditor,
        }

default_registry = TraitControlRegistry()


def trait_attribute_expression(trait, name, attr):
    value = getattr(trait.trait_type, attr)
    if isinstance(value, CodeType):
        return 'eval(object.traits()["%s"].trait_type.%s)' % (name, attr)
    else:
        return 'object.traits()["%s"].trait_type.%s' % (name, attr)

def TRangeEditor(trait, name):
    low_binding = bind('low', trait_attribute_expression(trait, name, '_low'))
    high_binding = bind('high', trait_attribute_expression(trait, name, '_high'))
    value_binding = bind('high', trait_attribute_expression(trait, name, '_high'))
        
    def widget(*args):
        args = (low_binding, high_binding,) + args
        return EnamlPyCall('SpinBox', *args)
        
    return widget

def TEnumEditor(trait, name):
    values_binding = bind('items', trait_attribute_expression(trait, name, 'values'))
        
    def widget(*args):
        args = (values_binding,) + args
        return EnamlPyCall('ComboBox', *args)
        
    return widget

class TraitsViewElement(HasTraits):

    registry = Instance(TraitControlRegistry)
    
    def _registry_default(self):
        return default_registry

class TItem(TraitsViewElement):
    #: the name of the trait the item is editing
    name = Str
    
    #: the label to display next to the control
    label = Str

    control = Any
    binding = Any(delegate)
    label_class = Any
    
    def __init__(self, name, *body, **kwargs):
        kwargs['name'] = name
        body += tuple(kwargs.get('body', ()))
        kwargs['body'] = body
        super(TItem, self).__init__(**kwargs)

    def build(self, object):
        print self.name
        trait = object.traits()[self.name]
        label = self.label_class(simple('text', repr(self.label)))
        binding = self.binding
        control = self.get_control(trait)(
            self.binding('value', 'object.'+self.name),
            bind('bg_color', "'error' if error else 'none'"),
            simple('read_only', str(not self.isWriteable(trait))),
            *self.body
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


class TraitsContainer(TraitsViewElement):
    #: the name of the container class to use
    container_class = Str("Form")
    
    #: the Enaml Python API widget factory for the container
    control = Property(Any, depends_on='container_class')
    
    #: the list of items
    items = List(Either(Str, TItem, Instance('TraitsContainer')))
    
    def __init__(self, *items, **kwargs):
        items += tuple(kwargs.get('items', ()))
        kwargs['items'] = list(items)
        super(TraitsContainer, self).__init__(**kwargs)
    
    def build(self, object):
        contents = []
        for item in self.items:
            if isinstance(item, basestring):
                # we just want default item for a trait
                contents += TItem(item).build(object)
            else:
                contents += item.build(object)
        return [self.control(*contents)]
    
    @cached_property
    def _get_control(self):
        return self.registry.widget_factories.setdefault(self.container_class,
                make_widget(self.container_class))

TForm = TraitsContainer

class THSplit(TraitsContainer):
    container_class = 'HSplit'

class TVSplit(TraitsContainer):
    container_class = 'VSplit'
    

class TView(TraitsContainer):
    container_class = "Window"

    items = List(Either(Str, TItem, TraitsContainer))

    def build(self, object):
        if not self.items:
            self.items = self.default_layout(object)
        return super(TView, self).build(object)
    
    def default_layout(self, object):
        items = [TItem(name=trait) for trait in sorted(object.trait_names())
                if trait[0] != '_' and trait != 'trait_added' and trait != 'trait_modified']
        form = TForm(*items)
        return [form]


@enaml_defn
def build(object, view=None):
    if view is None:
        view = TView()
    return view.build(object)[0]

        
def edit_traits(object, view=None):
    view = build(object, view)
    view.show(start_app=False)
    return view
    
def configure_traits(object, view=None):
    view = build(object, view)
    view.show()
