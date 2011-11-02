#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------

import ast
import re
import functools

import enaml
from .parser import enaml_ast, translate_operator
from .enaml_compiler import EnamlDefinition, DefnBodyCompiler
from .virtual_machine import evalcode

identifier_pattern = r'[_A-Za-z][_A-Za-z0-9]*'
number_pattern = r'-?[1-9][0-9]*'

lhs_matcher = re.compile(
    r'(?P<name1>' + identifier_pattern +
    r')((\[(?P<index>' + number_pattern +
    r')\])?\.(?P<name2>' + identifier_pattern +
    r'))?'
)

def get_expr(code):
    """ Given an expression string, return an ast.Expression object
    """
    return ast.parse(code, 'Enaml', mode='eval')

class EnamlPyDefn(object):
    """ Base class for the Enaml Python API defn AST builders
    """
    def __init__(self, name, args=None, defaults=None, body=None):
        self.name = name
        self.body = body if body is not None else []
        self.args = args if args is not None else []
        self.defaults = defaults if defaults is not None else []
    
    def ast(self):
        defaults = [get_expr(expr) for expr in self.defaults]
        parameters = enaml_ast.EnamlParameters(self.args, defaults)
        return enaml_ast.EnamlDefine(self.name, parameters,
            [body_item.ast() for body_item in self.body])

    def compile(self, global_ns):
        node = self.ast()
        exec('', global_ns, {}) # ensure builtins
        computed_defaults = []
        for expr in node.parameters.defaults:
            code = compile(expr, 'Enaml', mode='eval')
            computed = eval(code, global_ns)
            computed_defaults.append(computed)
            
        args = node.parameters.args 
        with enaml.imports():
            instructions = DefnBodyCompiler.compile(set(args), node.body)
        name = node.name
        definition = EnamlDefinition(
            name, instructions, args, computed_defaults, global_ns,
        )
        return definition


class EnamlPyCall(object):
    """ Base class for the Enaml Python API call AST builders
    """
    
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.body = args
        self.args = kwargs.get('args', [])
        self.kwargs = kwargs.get('kwargs', [])
        self.unpack = kwargs.get('unpack', [])
        self.captures = kwargs.get('captures', [])
    
    def ast(self):
        arguments = [enaml_ast.EnamlArgument(get_expr(arg))
                for arg in self.args] + \
            [enaml_ast.EnamlKeywordArgument(name, get_expr(expr))
                for name, expr in self.kwargs]
        captures = [enaml_ast.EnamlCaptures(name1, name2)
                for name1, name2 in self.captures]
        return enaml_ast.EnamlCall(self.name, arguments, self.unpack, captures,
            [body_item.ast() for body_item in self.body])


class EnamlPyAssignment(object):
    """ Base class for the Enaml Python API operator AST builders
    """
    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
    
    def ast(self):
        match = lhs_matcher.match(self.lhs)
        if match is None:
            raise SyntaxError('Invalid assignment left-hand side "%s"' % self.lhs)
        if match.group('index'):
            index = eval(match.group('index'))
            lhs = enaml_ast.EnamlGetattr(
                enaml_ast.EnamlIndex(match.group('name1'), index),
                match.group('name2')
            )
        elif match.group('name2'):
            lhs = enaml_ast.EnamlGetattr(
                enaml_ast.EnamlName(match.group('name1')),
                match.group('name2')
            )
        else:
            lhs = enaml_ast.EnamlName(match.group('name1'))
        
        rhs = enaml_ast.EnamlExpression(get_expr(self.rhs))
        
        return enaml_ast.EnamlAssignment(lhs, self.op, rhs)

# Utility Factories

class EnamlDefinitionDecorator(EnamlDefinition):
    """ A subclass of EnamlDefinition that acts as a decorator of a function that
    returns Python API objects.
    """

    def __init__(self, fn):
        self.fn = fn
        self.__name__ = fn.func_name
        self.__args__ = fn.func_code.co_varnames[:fn.func_code.co_argcount]
        self.__defaults__ = fn.func_defaults if fn.func_defaults is not None else []
        self.__globals__ = fn.func_globals
    
    def __enaml_call__(self, *args, **kwargs):
        body = self.fn(*args, **kwargs)
        if isinstance(body, EnamlPyCall):
            body = [body]
        body_ast = [body_item.ast() for body_item in body]
        code = DefnBodyCompiler.compile(set(self.__args__), body_ast)
        
        f_locals = self._build_locals(args, kwargs)
        f_globals = self.__globals__
        return evalcode(code, f_globals, f_locals)

enaml_defn = EnamlDefinitionDecorator

def make_widget(name):
    """ Utility function that creates a factory for widget calls
    """
    def widget(*args):
        if len(args) > 0 and isinstance(args[0], str):
            unpack = [args[0]]
            args = args[1:]
            return EnamlPyCall(name, unpack=unpack, *args)
        else:
            return EnamlPyCall(name, *args)
    return widget

def make_operator(symbol):
    op = translate_operator(symbol)
    def operator(lhs, rhs):
        return EnamlPyAssignment(lhs, op, rhs)
    return operator

simple = make_operator('=')
delegate = make_operator(':=')
bind = make_operator('<<')
notify = make_operator('>>')
        


