import os, shutil, subprocess, excmock, glob, re
from .common import BUILDBOT_ROOT

class AbstractDebBuilder:
    def __init__(self, tmpdir, packagename):
        """
        packagename     This argument is always prepended to the tmpdir. It
                        is possible to get string paths like /tmp/build_debs/python-38/python-38/bin,
                        but this is normal, because a /tmp/build_debs/python-38/src/ will also exist,
                        and the dpkg-deb program requires a virtual root of the same name as the
                        resulting package.
        """
        self.tmpdir = tmpdir
        self.packagename = packagename
    
    def build_deb_tree(self):
        """
        Builds a DEB tree under the folder selftmpdir+'/debtree' according to this
        deb-build's own logic.
        """
        raise NotImplementedError()
    
    def create_deb_file(self):
        """
        
        """
        raise NotImplementedError()
    
    def publish_deb_file(self):
        """
        
        """
        raise NotImplementedError()
    
    def convert_insys_to_debtree_path(self, insys_path, dst_root):
        """
        Converts a the path of a file that may exist in the current Unix
        installation, and returns the path that the file must have under
        some virtual root.
            insys_path      The path of the installed file.
            dst_root        The virtual root.
        Examples:
            convert_insys_to_debtree_path("/etc/fstab", "/tmp/building/package/package") == "/tmp/building/package/package/etc/fstab"
        """
        return os.path.join( dst_root, os.path.relpath(insys_path, start="/" ) )
    
    def pullin_tree(self, src, dst):
        """
        Copies an installed file to a virtual root, creating
        intermediate dirs if necessary.
            src     The path of the installed file.
            dst     The path to the virtual root.
        """
        # Get a list of every file under the prefix:
        files_under_prefix = glob.glob(
            os.path.join(src, "**"),
            recursive=True)
        # Calculate the root of the destination:
        dst_root = dst
        # Convert the source paths to destination paths:
        copylist = [
            {   'srcpath': src_path,
                'dstpath': self.convert_insys_to_debtree_path(src_path, dst_root),
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
        # Merge the source onto the debtree dir:
        self.pullin_tree(self.program_prefix, os.path.join(self.tmpdir, self.packagename, "debtree"))
