#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------

import unittest
import os

from ...exceptions import EnamlSyntaxError
from ...parsing.parser import parse
from ...parsing.renderer import ASTRenderer

class TestRenderer(unittest.TestCase):
    
    def process_directory(self, directory, callback):
        """Utility method to find all enaml files in a directory and call the callback on them"""
        if os.path.exists(directory) and os.path.isdir(directory):
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    if os.path.splitext(filename)[1] == '.enaml':
                        callback(os.path.join(dirpath, filename))
        else:
            raise IOError('Could not find directory at "%s"' % directory)
    
    def roundtrip_render(self, filename):
        """ Generate an AST from the filename, and render it without error
        """
        print 'processing', filename
        with file(filename) as fp:
            code = fp.read()
        try:
            ast = parse(code)
        except EnamlSyntaxError as exc:
            print 'bad example', filename
            return
        renderer = ASTRenderer()
        try:
            renderer.render(ast)
        except Exception as exc:
            self.fail('failed to render example "%s": %s' % (filename, exc))
        
    
    def roundtrip_parse_rendered(self, filename):
        """ Generate an AST from the filename, and render it, and parse the rendered code
        """
        print 'processing', filename
        with file(filename) as fp:
            code = fp.read()
        try:
            ast = parse(code)
        except EnamlSyntaxError as exc:
            print 'bad example', filename
            return
        renderer = ASTRenderer()
        rendered = renderer.render(ast)
        try:
            parse(rendered)
        except Exception as exc:
            self.fail('failed to re-parse rendered example "%s": %s' % (filename, exc))
    
    def test_examples(self):
        """ The renderer should render all examples without raising an exception.
        
        This test relies on being able to find the examples next to the
        main enaml directory, and will raise a warning if it can't find it.
        """
        import enaml
        filename = enaml.__file__
        enaml_dir, mod = os.path.split(filename)
        package_dir, subdir = os.path.split(enaml_dir)
        examples_dir = os.path.join(package_dir, 'examples')
        self.process_directory(examples_dir, self.roundtrip_render)
        self.process_directory(examples_dir, self.roundtrip_parse_rendered)
        