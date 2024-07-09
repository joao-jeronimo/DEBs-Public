import unittest, deb_building_lib, random, subprocess, os, shutil
from unittest.mock import patch

class TestFullPrefixDebBuilder(unittest.TestCase):
    """
    This tests the FullPrefixDebBuilder class, whose goels is to build
    a DEB package based on a full program prefix.
    """
    
    def deltree_if_exists(self, treepath):
        if os.path.isdir(treepath):
            shutil.rmtree(treepath)
    
    def setUp(self):
        self.abstract_debbuilder = deb_building_lib.debbuilders.AbstractDebBuilder(
            # Argument tmpdir may already include the package name. However,
            # the builder always prepends it again. This is because under
            # the outer diretory there will be the src and other directories:
            tmpdir          = "/tmp/unit_testing",
            packagename     = "progname",
            )
        self.full_prefix_debbuilder = deb_building_lib.debbuilders.FullPrefixDebBuilder(
            tmpdir          = "/tmp/unit_testing",
            program_prefix  = "/tmp/unit_testing_src/progname",
            packagename     = "progname",
            )
    def tearDown(self):
        self.deltree_if_exists("/tmp/unit_testing")
        self.deltree_if_exists("/tmp/unit_testing_src")
    
    @patch('excmock.raise_exception')
    @patch('subprocess.run')
    def test_build_deb_tree_pullsin_prefix(self, mock_subprocess_run, mock_raise_exception):
        """
        Make sure that this method creates the virtual deb-build tree
        under our tempdir.
        """
        # Fake a fake tree:
        os.makedirs('/tmp/unit_testing_src/progname')
        with open('/tmp/unit_testing_src/progname/config.txt', 'w') as expfile:
            expfile.write("papapa")
        os.makedirs('/tmp/unit_testing_src/progname/bin')
        with open('/tmp/unit_testing_src/progname/bin/progname', 'w') as expfile:
            expfile.write("tatatapopo")
        # Give orders to build the deb tree:
        self.full_prefix_debbuilder.build_deb_tree()
        # Assert that the tree was built as requested:
        self.assertTrue( os.path.isdir("/tmp/unit_testing/progname/debtree/tmp/unit_testing_src/progname/") )
        self.assertTrue( os.path.isfile("/tmp/unit_testing/progname/debtree/tmp/unit_testing_src/progname/config.txt") )
        self.assertTrue( os.path.isdir("/tmp/unit_testing/progname/debtree/tmp/unit_testing_src/progname/bin") )
        self.assertTrue( os.path.isfile("/tmp/unit_testing/progname/debtree/tmp/unit_testing_src/progname/bin/progname") )
    
    @patch('excmock.raise_exception')
    @patch('subprocess.run')
    def test_convert_insys_to_debtree_path(self, mock_subprocess_run, mock_raise_exception):
        """
        Make sure that the convert_insys_to_debtree_path() method returns
        correct results.
        """
        self.assertEqual(
            self.abstract_debbuilder.convert_insys_to_debtree_path("/etc/fstab", "/tmp/building/package/package"),
            "/tmp/building/package/package/etc/fstab"   )

if __name__ == '__main__':
    unittest.main(verbosity=2)
