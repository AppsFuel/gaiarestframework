import doctest
import unittest
list_of_doctests = []
list_of_unittests = ['author','book','genre']


def suite():
    suite = unittest.TestSuite()
    for t in list_of_doctests:
        suite.addTest(doctest.DocTestSuite(
            __import__(t, globals(), locals(), fromlist=["*"])
        ))
    for t in list_of_unittests:
        suite.addTest(unittest.TestLoader().loadTestsFromModule(
            __import__(t, globals(), locals(), fromlist=["*"])
        ))
    return suite