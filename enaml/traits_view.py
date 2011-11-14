#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------

from traits.api import HasTraits, Str, Any, List, Either, Instance, Property, cached_property

from .parsing.builders import EnamlPyCall, simple, delegate, enaml_defn, make_widget

_widget_factories = {}

class TraitsItem(HasTraits):
    control_class = Str("Field")
    control = Property(Any, depends_on=['_control', 'control_class'])
    _control = Any
    name = Str
    label = Str
    label_class = Any

    def build(self, model):
        return [
            self.label_class(
                simple('text', repr(self.label))
            ),
            self.control(
                delegate('value', 'model.'+self.name)
            )
        ]

    @cached_property
    def _get_control(self):
        if self._control is not None:
            return self._control
        else:
            return _widget_factories.setdefault(self.control_class,
                make_widget(self.control_class))
    
    def _set_control(self, value):
        self._control = value
    
    def _label_default(self):
        return self.name.replace('_', ' ').capitalize()+':'
    
    def _label_class_default(self):
        return make_widget('Label')

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
                if trait != 'trait_added' and trait != 'trait_modified']
        print [trait for trait in sorted(model.trait_names())
                if trait != 'trait_added' and trait != 'trait_modified']
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
