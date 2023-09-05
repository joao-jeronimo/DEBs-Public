import os, subprocess

class AbstractPreparer:
    def __init__(self, tmpdir):
        self.tmpdir = tmpdir
    
    def prepare(self):
        raise NotImplementedError()
    def cleanup(self):
        raise NotImplementedError()

class CMMIPreparer(AbstractPreparer):
    def __init__(self, tmpdir, tarball_url, configure_parms=[]):
        super(CMMIPreparer, self).__init__(tmpdir)
        self.tarball_url = tarball_url
        self.configure_parms = configure_parms
    
    def prepare(self):
        tarball_filepath = self.get_src_tarball(self.tarball_url)
        self.expand_src_tarball(tarball_filepath)
    
    def cleanup(self):
        pass
    
    def get_src_tarball(self, url):
        print("== Downloading %s . . ." % url)
        # Calculating names:
        out_filename = os.path.basename(url)
        destdir = os.path.join(self.tmpdir, 'src')
        out_filepath = os.path.join(destdir, out_filename)
        # Creating dirs:
        subprocess.run(
            args = [ 'mkdir', '-p', destdir, ],
            check = True,
            )
        # Downloading...
        self._static_get_tarball(url, out_filepath)
        return out_filepath
    
    def _static_get_tarball(self, url, destfilepath):
        print("== Downloading %s . . ." % url)
        # Downloading...
        subprocess.run(
            args = [
                'wget', '-c', url,
                '-O', destfilepath,
                ],
            check = True,
            )
    
    def expand_src_tarball(self, tarball_filepath):
        """
        tarballname     Omit the ".tar.?z" extension here
        extension       "tar.gz", "tar.bz2", "tar.xz", etc.
        """
        # Dump last 2 extension elements:
        extension = '.'.join(tarball_filepath.split('.')[-2:])
        # Where to expand to:
        dst_folderpath = os.path.dirname(tarball_filepath)
        # Do Extract:
        self._static_expand_tarball(tarball_filepath, extension, dst_folderpath)
        # TODO: Collect the list of expended files from TAR
        # command and return them as a list os paths.
    
    def _static_expand_tarball(self, tarball_filepath, extension, dst_folderpath):
        """
        tarballname     Full path of (maybe compressed) tarball, including extension.
        extension       "tar.gz", "tar.bz2", "tar.xz", etc.
        """
        # The format:
        if extension == 'tar':          flags = "xvf"
        elif extension == 'tar.gz':     flags = "xzvf"
        elif extension == 'tar.bz2':    flags = "xjvf"
        elif extension == 'tar.xz':     flags = "xJvf"
        else:                           raise NotImplementedError()
        # Prints:
        print("== Expanding %s . . ." % tarball_filepath)
        # Run command(s):
        subprocess.run(
            cwd = dst_folderpath,
            args = [
                'tar', flags, tarball_filepath,
                ],
            check = True,
            )
