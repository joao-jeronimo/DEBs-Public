import os, subprocess

class AbstractPreparer:
    def __init__(self, tmpdir):
        self.tmpdir = tmpdir
    
    def prepare(self):
        raise NotImplementedError()
    def cleanup(self):
        raise NotImplementedError()

class CMMIPreparer(AbstractPreparer):
    def __init__(self, tmpdir, tarball_url, program_prefix, configure_parms=[], src_dirname=None):
        super(CMMIPreparer, self).__init__(tmpdir)
        self.tarball_url        = tarball_url
        self.program_prefix     = program_prefix
        self.configure_parms    = configure_parms
        self.src_dirname        = src_dirname
    
    def prepare(self):
        # Fetch and expand tarball:
        tarball_filepath = self.get_src_tarball(self.tarball_url)
        self.expand_src_tarball(tarball_filepath)
        # Calculate the name of the tarball-extracted dir, if not provided by the factory:
        if not self.src_dirname:
            # Strip the path from the tarball fullpath:
            tarball_basename = os.path.basename(tarball_filepath)
            # Strips the extension to get to a default extracted-folder name:
            self.src_dirname = '.'.join(tarball_filepath.split('.')[0:-2])
        # Calculate the fullpath thereof:
        tarball_folderpath = os.path.dirname(tarball_filepath)
        source_rootpath = os.path.join(tarball_folderpath, self.src_dirname)
        # Run the "configure" script:
        self.run_configure(source_rootpath=source_rootpath, prefix=self.program_prefix, configflags=self.configure_parms)
    
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
    
    def run_configure(self, source_rootpath, prefix, configflags=[]):
        # Paths relative to CWD:
        configure_filepath = os.path.join(source_rootpath, 'configure', )
        # Run command(s):
        self._static_run_configure(
            configure_filepath  = configure_filepath,
            prefix              = prefix,
            build_dirpath       = None,         # Build the tarball in-source.
            configflags         = configflags,
            )
    
    def _static_run_configure(self, configure_filepath, prefix, build_dirpath=None, configflags=[]):
        # CWD for subprocess:
        if not build_dirpath:
            build_dirpath = os.path.dirname(configure_filepath)
        working_dir = build_dirpath
        # Other params:
        prefix_spec = ('--prefix=%s' % prefix)
        # Prints:
        print("== Running %s %s . . ." % (configure_filepath, prefix_spec, ) )
        # Run command(s):
        subprocess.run(
            cwd = working_dir,
            args = [
                configure_filepath, prefix_spec,
                *configflags,
                ],
            check = True,
            )
        # Configure may end in error but still return 0, so check if the Makefile was created:
        if not os.path.isfile(os.path.join(build_dirpath, 'Makefile')):
            raise ConfigureError("Error running «%s»: no Makefile created" % " ".join([configure_filepath, prefix_spec, *configflags, ]))
