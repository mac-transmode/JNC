"""
Created on 20 jul 2012

@author: emil@tail-f.com

PyUnit is needed to run these tests.

To run, stand in project dir and enter:
$ python -m unittest discover -v
"""
import unittest

from pyang.plugins import jpyang  #@UnresolvedImport
from pyang.tests import util  #@UnresolvedImport
import copy


class Test(unittest.TestCase):
    """Contains tests for methods in JPyang.JavaMethod"""

    def setUp(self):
        """Runs before each test"""
        # Construct a statement tree rooted at self.m, and method generators
        util.init_context(self)
        util.create_statement_tree(self)
        util.create_method_generators(self)

    def tearDown(self):
        """Runs after each test"""
        pass

    def testSetUp(self):
        """Statement tree and generators are properly constructed"""
        util.test_default_context(self)
        util.test_statement_tree(self)
        util.test_method_generators(self)

    def testInit(self):
        """Values and references correct in Java Methods of different origin"""
        # Create method with default settings
        method1 = jpyang.JavaMethod()
        assert method1.exact is None
        assert method1.javadocs == []
        assert method1.modifiers == []
        assert method1.return_type is None
        assert method1.name is None
        assert method1.parameters == []
        assert method1.exceptions == []
        assert method1.body == []
        assert method1.indent == ' ' * 4
        
        # Create empty constructor method for container statement c
        method2 = self.cgen.empty_constructor()
        assert method2.exact is None
        assert method2.javadocs
        assert 'public' in method2.modifiers
        assert method2.return_type is None
        assert method2.name == self.cgen.n
        assert method2.parameters == []
        assert method2.exceptions == []
        assert method2.body
        assert method2.indent == ' ' * 4
        
        # Check that no references are shared, even for empty lists
        assert method1.javadocs is not method2.javadocs
        assert method1.modifiers is not method2.modifiers
        assert method1.parameters is not method2.parameters
        assert method1.parameters == method2.parameters
        assert method1.exceptions is not method2.exceptions
        assert method1.exceptions == method2.exceptions
        assert method1.body is not method2.body
        assert method1.indent is not method2.indent
        assert method1.indent == method2.indent

    def testEq(self):
        """Equality checks with == and != works as expected"""
        method = clone = self.cgen.empty_constructor()
        assert method is clone, 'Sanity check: same reference'
        assert method == clone, 'Sanity check: equal objects'
        assert not method != clone, 'Sanity check: equal objects'
        clone2 = self.cgen.empty_constructor()
        assert method is not clone2, 'Different reference'
        assert method == clone2, 'But still equal'
        clone2.return_type = 'bogus'
        assert method != clone2, 'return_type matters for equality'
        assert not method == clone2, 'check both __eq__ and __ne__'

    def testShares_mutables_with(self):
        """Clones have equal string representation but different reference"""
        method = self.cgen.empty_constructor()
        clone = copy.deepcopy(method)
        shallow = copy.copy(method)
        assert method is not clone, 'Different reference'
        assert method is not shallow, 'Different reference'
        assert method == clone, 'But still equal'
        assert method == shallow, 'But still equal'
        assert method.as_string() == clone.as_string(), 'Same string repr'
        assert method.as_string() == shallow.as_string(), 'Same string repr'
        assert not method.shares_mutables_with(clone)
        assert method.shares_mutables_with(shallow)
        clone.return_type = 'bogus'
        assert not method == clone, 'return_type matters for equality'
        clone.return_type = None
        assert method == clone, 'Should be equal again'
        del clone.return_type
        assert not method == clone, 'Not equal if attribute is missing'
        clone.return_type = None
        assert method == clone, 'Should be equal again'
        clone.javadocs = method.javadocs
        assert method.shares_mutables_with(clone), 'javadoc is shared'
        del clone.javadocs
        assert not hasattr(clone, 'javadocs'), 'deleted from clone'
        assert hasattr(method, 'javadocs'), 'not deleted from method'
        assert not method.shares_mutables_with(clone), 'Not sharing anymore'
        

if __name__ == "__main__":
    """Launch all unit tests"""
    #import sys;sys.argv = ['', 'Test.testCapitalize_first']  # Only one
    unittest.main()