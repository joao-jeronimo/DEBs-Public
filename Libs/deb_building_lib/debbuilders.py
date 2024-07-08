import os, shutil, subprocess, excmock

class AbstractDebBuilder:
    def __init__(self, tmpdir):
        self.tmpdir = tmpdir
    
    def build_deb_tree(self):
        """
        Builds a DEB tree under the folder selftmpdir+'/debtree' according to this
        deb-build's own logic.
        """
        raise NotImplementedError()

class FullPrefixDebBuilder(AbstractDebBuilder):
    """
    A DEB-file builder that takes a single folder path as a parameters and
    puts inside the DEB file everything that is directly or indirectly
    under that tree.
    """
    
    def __init__(self, tmpdir, program_prefix):
        super(FullPrefixDebBuilder, self).__init__(tmpdir)
        self.program_prefix     = program_prefix
    
    def build_deb_tree(self):
        """
        Builds a DEB tree under the folder selftmpdir+'/debtree' based on the
        prefix passed-in through the constructor.
        """
        pass
