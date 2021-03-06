from abc import ABCMeta, abstractmethod

from traits.api import Any, TraitChangeNotifyWrapper, TraitType


#------------------------------------------------------------------------------
# Expression default trait
#------------------------------------------------------------------------------
class ExpressionDefaultTrait(TraitType):
    """ A custom trait type that handles initializing a component
    trait attribute with a value computed from an expression. This
    allows expression to depend upon values which should be computed
    via expressions (and so on) to initialize properly without needing
    an explicit dependency graph to handle it.

    """
    @staticmethod
    def mangle(name):
        """ A static method which will mangle a name to create a 
        storage space in an objects __dict__. For a given string,
        this method will always return the same mangled name.

        """
        return '_expr_default_' + name

    def __init__(self, expression):
        """ Initialize an expression default trait.

        Parameters
        ----------
        expression : Instance(AbstractExpression)
            An instance of an expression object that will provide the
            default value when evaluated.

        """
        super(ExpressionDefaultTrait, self).__init__()
        self.expression = expression

    def get(self, obj, name):
        """ Called to get the value for the trait. The first time
        this is called, it will eval the expression and store the 
        value in the objects __dict__. Future calls, will return
        the value stored in the __dict__.

        """
        name = self.mangle(name)
        dct = obj.__dict__
        if name in dct:
            res = dct[name]
        else:
            res = dct[name] = self.expression.eval_expression()
        return res


#------------------------------------------------------------------------------
# Setup hooks 
#------------------------------------------------------------------------------
class AbstractSetupHook(object):
    """ An abstract base class that defines the methods that need to 
    be implemented by a setup hook that is used by a Component during
    the setup process.

    """
    __metaclass__ = ABCMeta

    __slots__ = ()
    
    @abstractmethod
    def create(self, component):
        raise NotImplementedError
    
    @abstractmethod
    def initialize(self, component):
        raise NotImplementedError

    @abstractmethod
    def bind(self, component):
        raise NotImplementedError


class NullSetupHook(AbstractSetupHook):
    """ An AbstractSetupHook implementation that does nothing. This 
    makes is easy for hooks that only need to implement a few methods 
    to subclass from this and implement only what is needed.

    """
    __slots__ = ()
    
    def create(self, component):
        yield

    def initialize(self, component):
        yield

    def bind(self, component):
        yield


class ExpressionSetupHook(NullSetupHook):

    __slots__ = ('name', 'expression', 'eval_default')

    def __init__(self, name, expression, eval_default=True):
        self.name = name
        self.expression = expression
        self.eval_default = eval_default

    def create(self, component):
        """ A setup hook method which sets up the expression yields
        back to the framework for widget creation, and then finalizes
        the expression.

        """
        # We want to setup the expressions before we create and
        # initialize the widgets so that values computed from the
        # expression can be used to select an appropriate widget
        # if necessary.
        self.setup_expression(component)
        
        # Yield back to the framework so it can create the widgets in 
        # the tree. By the time this function is resumed, all of the
        # widgets in the tree will have been created.
        yield

        # Now that all of the widgets have been created, we are done
        # with the process of creating objects in the tree. So, we
        # can safetly evaluate our expression and assign its value
        # to the attribute on the component, removing any instance
        # traits we needed to add for initialization to work properly.
        self.finalize_expression(component)

    def bind(self, component):
        """ A setup hook method which allows the widget event handlers
        to be bound, then sets up the notifiers for the expression.

        """
        # The last thing we need to do in the setup process is parse the
        # expression and bind the updated listeners. We do this after 
        # the ui toolkit has finished binding its own event handlers.
        yield
        self.expression.bind()
        
    def setup_expression(self, component):
        """ Sets up the expression for use on a component. This involves
        adding special temporary instance traits to the component so 
        that the default value is properly retrieved from the expression.

        """
        name = self.name
        expression = self.expression
        eval_default = self.eval_default

        # If the trait is in the class traits, then we need to add an 
        # instance trait temporarily in order to handle the default
        # value initialization. Unlike the cases which are handled below,
        # where we are creating a new trait, there is notifier management
        # that needs to take place here since the trait may already have
        # notifiers associated with it. Also, for things like property
        # traits and delegates, simple setting the default value method
        # won't work. So, we add an Any and later on do setattr with the
        # computed value after we remove the Any trait. The eval default
        # flag indictates we have an expression that is right associative
        # and so we don't care about the value of the expression.
        if name in component.class_traits():
            if eval_default:
                component.add_trait(name, ExpressionDefaultTrait(expression))
            else:
                # we don't need to do anything special
                pass

        # Otherwise, the user is defining their own attributes and we 
        # need to create an instance trait (if necessary, since it may have
        # been done once already) and then bind the default value (also if 
        # necessary). Note that the .add_trait method automatically clones 
        # the trait before adding it to the instance trait dict. This means 
        # that the default value handler must be applied *before* the call 
        # to .add_trait. We don't need to be rigorous about notifiers like
        # in the other cases, because the .add_trait method handles the 
        # notifier management for us.
        else:
            trait = component._instance_traits().get(name)
            if trait is None:
                trait = Any().as_ctrait()
            if eval_default:
                dvf = lambda obj: expression.eval_expression()
                trait.default_value(8, dvf)
            component.add_trait(name, trait)

    def finalize_expression(self, component):
        """ Finalizes the expression object by computing its value if 
        required, removing any appropriate instance traits, and setting
        the value on component.

        """
        # This method is called after all the widgets in the tree have
        # been built and there should be no other objects needing to 
        # be created on which this expression may depend. This means
        # it's safe to grab the value of the expression and remove
        # the ExpressionDefaultTrait instance trait (if one was added)
        # and assign the expression value to the component (now on the
        # class trait). This should ensure that things like delegates
        # and Properties get initialized properly.
        name = self.name
        eval_default = self.eval_default

        if eval_default:
            val = getattr(component, name)

        # When removing an instance traits (as opposed to adding one)
        # we need to manually manage our notifiers. The default behavior
        # of traits where it doesn't copy the notifiers is correct, but
        # since we are using instance traits like they are invisible, 
        # those semantics are not what we want. So, we are left with this
        # manual management.
        itrait = component._instance_traits().get(name)
        if itrait is not None:
            if isinstance(itrait.trait_type, ExpressionDefaultTrait):
                component.remove_trait(name)
                inotifiers = itrait._notifiers(0)
                if inotifiers is not None:
                    class_trait = component.trait(name)
                    if class_trait is not None:
                        for notifier in inotifiers:
                            self.rebind(component, name, notifier)
        
        # Set the trait quietly so no notifiers are run. Remember that
        # we want the process to be invisible to the user and appear
        # like any other default value assignment.
        if eval_default:
            component.trait_setq(**{name: val})

    def rebind(self, obj, name, notifier):
        """ Rebinds a HasTraits object's TraitChangeNotifyWrapper for 
        the trait of the given name.

        """
        if isinstance(notifier, TraitChangeNotifyWrapper):
            call_method = notifier.call_method
            if call_method.startswith('call_'):
                handler = notifier.handler
            elif call_method.startswith('rebind_call_'):
                # The handler object is stored as a weakref
                handler_obj = notifier.object()
                if handler_obj is None:
                    return
                handler_name = notifier.name
                handler = getattr(handler_obj, handler_name)
            else:
                msg = 'unknown call method `%s`' % call_method
                raise ValueError(msg)
            obj.on_trait_change(handler, name)

