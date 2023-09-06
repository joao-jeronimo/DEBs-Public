import unittest, deb_building_lib

class TestCMMIPreparer(unittest.TestCase):

    def setUp(self):
        self.cmmi_preparer = deb_building_lib.preparers.CMMIPreparer(
            tmpdir          = "/tmp/unit_testing",
            tarball_url     = "https://www.example.com/path1/path2/Composite-program-name-7.4.2.tar.gz",
            program_prefix  = "",
            configure_parms = [],
            )

    def test_file_extension(self):
        self.assertEqual(self.cmmi_preparer.file_extension("Composite-program-name-7.4.2.tar.gz"), 'tar.gz')
    def test_file_plainname(self):
        self.assertEqual(self.cmmi_preparer.file_plainname("Composite-program-name-7.4.2.tar.gz"), 'Composite-program-name-7.4.2')

if __name__ == '__main__':
    unittest.main(verbosity=2)
