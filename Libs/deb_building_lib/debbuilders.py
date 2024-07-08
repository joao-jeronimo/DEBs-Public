import os, shutil, subprocess, excmock, glob, re

class AbstractDebBuilder:
    def __init__(self, tmpdir, packagename):
        self.tmpdir = tmpdir
        self.packagename = packagename
    
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
    
    def __init__(self, tmpdir, packagename, program_prefix):
        super(FullPrefixDebBuilder, self).__init__(tmpdir, packagename)
        self.program_prefix     = program_prefix
    
    def build_deb_tree(self):
        """
        Builds a DEB tree under the folder selftmpdir+'/debtree' based on the
        prefix passed-in through the constructor.
        """
        # Get a list of every file under the prefix:
        files_under_prefix = glob.glob(
            os.path.join(self.program_prefix, "**"),
            recursive=True)
        # Calculate the root of the destination:
        dst_root = os.path.join(self.tmpdir, self.packagename, "debtree")
        # Convert the source paths to destination paths:
        copylist = [
            {   'srcpath': src_path,
                'dstpath': os.path.join( dst_root, os.path.relpath(src_path, start=self.program_prefix ) ),
                }
            for src_path in files_under_prefix
            ]
        # Copy 'em all:
        for instr in copylist:
            # Calculate the parent of the destination dir:
            dst_parent = os.path.dirname(instr['dstpath'])
            # Make sure the parent exists:
            os.makedirs(dst_parent, exist_ok=True)
            # Copy the file is we have here a file:
            if os.path.isfile( instr['srcpath'] ):
                shutil.copyfile( instr['srcpath'], instr['dstpath'] )
