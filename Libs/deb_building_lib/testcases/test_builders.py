import unittest, deb_building_lib, random, subprocess
from unittest.mock import patch

class TestFullPrefixDebBuilder(unittest.TestCase):
    """
    This tests the FullPrefixDebBuilder class, whose goels is to build
    a DEB package based on a full program prefix.
    """

    def setUp(self):
        self.full_prefix_debbuilder = deb_building_lib.debbuilders.FullPrefixDebBuilder(
            tmpdir          = "/tmp/unit_testing",
            program_prefix  = "/opt/progname",
            )
    
    @patch('excmock.raise_exception')
    @patch('subprocess.run')
    @patch('builtins.print')
    def test_build_deb_tree(self, mock_print, mock_subprocess_run, mock_raise_exception):
        """
        Make sure that this method creates the virtual deb-build tree
        under our tempdir.
        """
        self.assertIsNone( self.full_prefix_debbuilder.build_deb_tree() )

if __name__ == '__main__':
    unittest.main(verbosity=2)
