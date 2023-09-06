import os, shutil, subprocess

class AbstractPreparer:
    def __init__(self, tmpdir):
        self.tmpdir = tmpdir
    
    def _rmdir_and_check(self, dirpath):
        print("Deleting directory %s . . ." % dirpath)
        if not os.getenv('IGNORE_REMOVE_ERRORS', False):
            assert os.path.isdir(dirpath)
        #shutil.rmtree(dirpath, ignore_errors=False, onerror=None)
        subprocess.run(
            args = [ 'sudo', 'rm', '-rf', dirpath, ],
            check = True,
            )
        assert not os.path.exists(dirpath)
    
    def _assert_file_absence(self, dirname):
        if os.path.exists(dirname):
            raise Exception("File or dorectory «%s» already exists!" % dirname)
    
    def prepare(self):
        raise NotImplementedError()
    def cleanup(self):
        self._rmdir_and_check(self.tmpdir)

class CMMIPreparer(AbstractPreparer):
    def __init__(self, tmpdir, tarball_url, program_prefix, configure_parms=[], src_dirname=None):
        super(CMMIPreparer, self).__init__(tmpdir)
        self.tarball_url        = tarball_url
        self.program_prefix     = program_prefix
        self.configure_parms    = configure_parms
        self.src_dirname        = src_dirname
        # Calculate the name of the tarball-extracted dir, if not provided by the factory:
        if not self.src_dirname:
            # If not present, this is by default the same name of the tarball, but without extensions:
            # Strip the web path from the tarball fullpath:
            tarball_basename = os.path.basename(tarball_url)
            # Find the extension-less file name:
            self.src_dirname = self.file_plainname(tarball_basename)
        # This var is used to assert that a pre-existing folder is NOT
        # being «rm -rf»'d duraing cleanup.
        self.prefix_folder_precedes_install = os.path.exists(self.program_prefix)
    
    def _check_prepare_preconditions(self):
        # Check facts about files:
        self._assert_file_absence(self.program_prefix)
        self._assert_file_absence(self.src_dirname)
    
    COMPOSITE_EXTENSION_ELEMENTS = [ 'tar', 'gz', 'bz2', 'xz', ]
    
    def file_extension(self, filename):
        """
        Extracts an extension from a filename.
        """
        # Split the filename by the period:
        splitted_filename = filename.split('.')
        # Filenames with no perior have no extension:
        if len(splitted_filename) == 1:
            return ""
        # In most cases, the extension is the last element:
        file_extension = splitted_filename[-1]
        # An exception if made for a set of extensions, where a different algorithm is ran:
        if file_extension not in self.COMPOSITE_EXTENSION_ELEMENTS:
            return file_extension
        # Different algorithm is: extenstion is last N elements, for
        # gratest N for which every element is a composite extension:
        extension_elem_i = len(splitted_filename)-1
        assert splitted_filename[extension_elem_i] in self.COMPOSITE_EXTENSION_ELEMENTS
        while splitted_filename[extension_elem_i-1] in self.COMPOSITE_EXTENSION_ELEMENTS:
            extension_elem_i -= 1
        # Build and return the finale:
        extension_splitted = splitted_filename[extension_elem_i:]
        final_extension = '.'.join(extension_splitted)
        return final_extension
    def file_plainname(self, filename):
        """
        Extracts the "name" part from a filename that has an extension.
        """
        extension  = self.file_extension(filename)
        extension_str_i = len(filename) - len(extension)
        plainname = filename[:extension_str_i-1]
        return plainname
    
    def prepare(self):
        if os.getenv("SKIP_CMMI_PRAPARE", False):
            # Set this var to True se that the cleanup can still work correctly:
            self.prefix_folder_precedes_install = False
            return
        self._check_prepare_preconditions()
        # Fetch tarball and calculate it's parent dir:
        tarball_filepath = self.get_src_tarball(self.tarball_url)
        tarball_folderpath = os.path.dirname(tarball_filepath)
        if not os.getenv("SKIP_CMMI_EXPAND", False):
            # Expand the tarball:
            self.expand_src_tarball(tarball_filepath)
        # Calculate the fullpath of the folder that was inside the tarball:
        source_rootpath = os.path.join(tarball_folderpath, self.src_dirname)
        if not os.getenv("SKIP_CMMI_CONFIGURE", False):
            # TODO: Check source_rootpath against the return value of expand_src_tarball()..
            # Run the "configure" script:
            self.run_configure(source_rootpath=source_rootpath, prefix=self.program_prefix, configflags=self.configure_parms)
        # Run "make":
        self.build_tarball( os.path.join(source_rootpath, "Makefile") )
        # Run "make install":
        self.install_tarball( os.path.join(source_rootpath, "Makefile") )
    
    def cleanup(self):
        super(CMMIPreparer, self).cleanup()
        if not os.getenv("SKIP_CMMI_CLEANUP", False):
            assert( self.prefix_folder_precedes_install == False )
            self._rmdir_and_check(self.program_prefix)
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
    
    ###################################################################
    ##### Running configure:                ###########################
    ###################################################################
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

    ###################################################################
    ##### Building:                         ###########################
    ###################################################################
    def build_tarball(self, makefile_filepath):
        makefile_folderpath = os.path.dirname(makefile_filepath)
        self._static_cmmi_build(makefile_folderpath)
    
    def _static_cmmi_build(self, makefile_folderpath):
        # Prints:
        print("== Building on '%s' . . ." % makefile_folderpath)
        # Run command(s):
        subprocess.run(
            cwd = makefile_folderpath,
            args = [ 'make', '-j3', ],
            check = True,
            )

    ###################################################################
    ##### Installing:                       ###########################
    ###################################################################
    def install_tarball(self, makefile_filepath, destination=None):
        # See if the "prefix" foldeer alread exists:
        self.prefix_folder_precedes_install = os.path.exists(self.program_prefix)
        # Call the makefile to install:
        makefile_folderpath = os.path.dirname(makefile_filepath)
        self._static_cmmi_install(makefile_folderpath, destination=destination)
    
    def _static_cmmi_install(self, makefile_folderpath, destination=None):
        # Paths absolute or relative to CWD:
        if destination:
            abs_destination = os.path.abspath(destination)
        else:
            abs_destination = None
        # Prints:
        print("== Installing . . .")
        # Run command(s):
        subprocess.run(
            cwd = makefile_folderpath,
            #env = environ,
            args = [
                'sudo', #'--preserve-env)%s'%','.join(environ.keys()),
                'make', *(['DESTDIR=%s' % abs_destination] if abs_destination else []), 'install',
                ],
            check = True,
            )
        if destination:
            subprocess.run(
                args = [ 'sudo', 'chown', 'jj:jj', '-Rc', destination, ],
                check = True,
                )