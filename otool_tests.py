import os
import otool
import unittest
import tempfile

class OtoolTestCase(unittest.TestCase):

    # Test method
    def test_empty(self):
        """Just a simple test case."""
        otool.app.testing = True
        self.app = otool.app.test_client()
        rv = self.app.get('/otool/')
        assert '<head>' in rv.data

if __name__ == '__main__':
    unittest.main()