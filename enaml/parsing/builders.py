#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------

import ast
import re

from .parsing.parser import parser
from .parsing import enaml_ast

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
    return ast.parse(code).body[0]

class EnamlPyDefn(object):
    """ Base class for the Enaml Python API defn AST builders
    """
    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.body = args
        self.args = kwargs.get('args', [])
        self.defaults = kwargs.get('defaults', [])
    
    def ast(self):
        defaults = [get_expr(expr) for expr in self.defaults]
        parameters = enaml_ast.EnamlParameters(self.args, defaults)
        return enaml_ast.EnamlDefine(self.name, parameters,
            [body_item.ast() for body_item in self.body])

class EnamlPyWidget(object):
    """ Base class for the Enaml Python API widget AST builders
    """
    
    def __init__(self, *args, **kwargs):
        self.body = args
        self.args = kwargs.get('args', [])
        self.kwargs = kwargs.get('kwargs', [])
        self.unpack = kwargs.get('unpack', [])
        self.captures = kwargs.get('captures', [])
    
    @property
    def name(self):
        """ Return the class name
        """
        return self.__class__.__name__
    
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
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
    
    def ast(self):
        match = lhs_matcher(self.lhs)
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

class Default(EnamlPyAssignment):
    op = '='

class Delegate(EnamlPyAssignment):
    op = ':='

class Bind(EnamlPyAssignment):
    op = '<<'

class Notify(EnamlPyAssignment):
    op = '>>'


