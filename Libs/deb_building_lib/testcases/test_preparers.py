import unittest, deb_building_lib, random
from unittest.mock import patch

class TestCMMIPreparer(unittest.TestCase):

    def setUp(self):
        self.cmmi_preparer = deb_building_lib.preparers.CMMIPreparer(
            tmpdir          = "/tmp/unit_testing",
            tarball_url     = "https://www.example.com/path1/path2/Composite-program-name-7.4.2.tar.gz",
            program_prefix  = "",
            configure_parms = [],
            )

    def test_file_extension(self):
        """
        Test the calculaton of the compressed filename extensions.
        """
        self.assertEqual(self.cmmi_preparer.file_extension("Composite-program-name-7.4.2.tar.gz"), 'tar.gz')
    def test_file_plainname(self):
        """
        Test the removal of compressed filename extensions.
        """
        self.assertEqual(self.cmmi_preparer.file_plainname("Composite-program-name-7.4.2.tar.gz"), 'Composite-program-name-7.4.2')
    
    def test_prefix_folder_precedes_install(self):
        """
        Tests that the prefix_folder_precedes_install field is correctly set.
        (4 relevant cases)
        """
        PROPOSED_PROGRAM_PREFIX = "/tmp/build-to-here-%07d" % (10000000*random.random(), )
        # When the folder does not exist:
        the_preparer = deb_building_lib.preparers.CMMIPreparer(tmpdir="NA", tarball_url="NA", program_prefix=PROPOSED_PROGRAM_PREFIX)
        self.assertFalse( the_preparer.prefix_folder_precedes_install )
        # When the SKIP_CMMI_PREPARE envvar is set to True:
        the_preparer.prefix_folder_precedes_install = True
        with patch.dict("os.environ", { 'SKIP_CMMI_PREPARE': "1", }) as mock_getenv:
            the_preparer.prepare()
        self.assertFalse( the_preparer.prefix_folder_precedes_install )
    
    @patch('excmock.raise_exception')
    @patch('subprocess.run')
    @patch('builtins.print')
    def test_prepare_uncompresses_tarball(self, mock_print, mock_subprocess_run, mock_raise_exception):
        """
        Tests that the prepare() actually expands tha tarball as requested.
        """
        # Tests when SKIP_CMMI_PREPARE envvar is NOT there:
        with patch.dict("os.environ", { }) as mock_getenv:
            self.cmmi_preparer.prepare()
            mock_subprocess_run.assert_has_calls(
                calls=[
                    unittest.mock.call(
                        *[          # args
                            ],    
                        **{         # kwargs
                            'cwd'       : "/tmp/unit_testing/src",
                            'args'      : [ 'tar', 'xzvf', '/tmp/unit_testing/src/Composite-program-name-7.4.2.tar.gz', ],
                            #'env'      : {},
                            #'stdout'    : None,
                            #'stderr'    : None,
                            'check'     : True,
                            },
                        )
                    ],
                any_order=False,
                )
        # Tests when SKIP_CMMI_PREPARE envvar is there with a 0 value:
        with patch.dict("os.environ", { 'SKIP_CMMI_PREPARE': "0", }) as mock_getenv:
            self.cmmi_preparer.prepare()

if __name__ == '__main__':
    unittest.main(verbosity=2)
