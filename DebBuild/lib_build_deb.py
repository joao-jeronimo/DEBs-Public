import subprocess, os, glob

class ConfigureError(Exception):
    pass

#####################################################################
##### Instaling build dependencies:                          ########
#####################################################################
def apt_install_package(*packages):
    subprocess.run(
        args = [
            'sudo',
            'apt-get', 'install', *packages,
            ],
        check = True,)
def apt_install_build_deps_for(*packages):
    subprocess.run(
        args = [
            'sudo',
            'apt-get', 'build-dep', *packages,
            ],
        check = True,)

#####################################################################
##### Making build directories and building programs:        ########
#####################################################################
def mkbuilddirs():
    os.makedirs("../builds/src", exist_ok=True)
    os.makedirs("../builds/build", exist_ok=True)
    os.makedirs("../builds/installed", exist_ok=True)

def get_src_tarball(url):
    print("== Downloading %s . . ." % url)
    out_filename = os.path.basename(url)
    subprocess.run(
        args = [
            'wget', '-c', url,
            '-O', os.path.join(os.path.pardir, 'builds', 'src', out_filename),
            ],
        check = True,)

def expand_src_tarball(tarballname, extension):
    """
    tarballname     Omit the ".tar.?z" extension here
    extension       "tar.gz", "tar.bz2", "tar.xz", etc.
    """
    # CWD for subprocess, relative to script:
    srcpath = os.path.join(os.path.pardir, 'builds', 'src', )
    # Paths relative to CWD:
    #(none)
    # Other params:
    if extension == 'tar':          flags = "xvf"
    elif extension == 'tar.gz':     flags = "xzvf"
    elif extension == 'tar.bz2':    flags = "xjvf"
    elif extension == 'tar.xz':     flags = "xJvf"
    else:                           raise NotImplementedError()
    tarball_filename = (tarballname+'.'+extension)
    # Prints:
    print("== Expanding %s . . ." % tarball_filename)
    # Run command(s):
    subprocess.run(
        cwd = srcpath,
        args = [
            'tar', flags, tarball_filename,
            ],
        check = True,
        )

def configure_tarball(tarballname, prefix, configflags=[]):
    # CWD for subprocess, relative to script:
    builddir = os.path.join(os.path.pardir, 'builds', 'build', tarballname, )
    # Paths relative to CWD:
    configure_path = os.path.join(os.path.pardir, os.path.pardir, 'src', tarballname, 'configure', )
    # Other params:
    prefix_spec = ('--prefix=%s' % prefix)
    # Prints:
    print("== Running %s %s . . ." % ( os.path.join(builddir, configure_path), prefix_spec, ) )
    # Run command(s):
    os.makedirs(builddir, exist_ok=True)
    subprocess.run(
        cwd = builddir,
        args = [
            configure_path, prefix_spec,
            *configflags,
            ],
        check = True,
        )
    # configure may end in error but stiff return 0, so check if the mkefile was created:
    if not os.path.isfile(os.path.join(builddir, 'Makefile')):
        raise ConfigureError("Error running %s." % " ".join([configure_path, prefix_spec, *configflags, ]))

def build_tarball(tarballname):
    builddir = os.path.join(os.path.pardir, 'builds', 'build', tarballname, )
    subprocess.run(
        cwd = builddir,
        args = [ 'make', '-j3', ],
        check = True,
        )

def install_tarball(tarballname, destination):
    builddir = os.path.join(os.path.pardir, 'builds', 'build', tarballname, )
    subprocess.run(
        cwd = builddir,
        args = [ 'make', ('DESTDIR=%s' % destination), 'install', ],
        check = True,
        )

#####################################################################
##### Building DEB files:                ############################
#####################################################################
control_file_template = (
"""Package: %(pkgname)s
Version: %(version)s
Depends: %(dependencies)s
Architecture: %(arch)s
Maintainer: %(maintainer)s
Description: %(description)s
""")

def rsynch_full_path(src, dst):
    # Calculate the destination filepath so that we can mkdir it:
    dstdir = os.path.dirname(dst)
    # Mksure the dir exists:
    subprocess.check_call(['mkdir', '-p', dstdir])
    # Rsync asked stuff:
    subprocess.check_call(['rsync', '-rlt', '--delete', '--itemize-changes', '-Rv', src, dst])

def build_deb_from_files(debfile, packagename, version, maintainer, dependencies, description, pathlist):
    # Mksure the dir exists:
    subprocess.check_call(['mkdir', '-p', packagename])
    # Copy the future package contentes theire:
    for onepath in pathlist:
        rsynch_full_path(
            src = onepath,
            dst = (packagename + os.path.sep),
            )
    # Control file name:
    controlfile_name = os.path.join(packagename, "DEBIAN", "control")
    subprocess.check_call(['mkdir', '-p', os.path.dirname(controlfile_name)])
    # Generate the control file:
    with open( controlfile_name, "w" ) as outcontrol:
        outcontrol.write(control_file_template % {
            'pkgname'           : packagename,
            'version'           : version,
            'dependencies'      : ", ".join(dependencies),
            'arch'              : "all",
            'maintainer'        : maintainer,
            'description'       : description,
            })
    # Invoke dpkg-deb:
    subprocess.check_call([
        'dpkg-deb', '--build', '--root-owner-group',
        packagename, debfile, ])

def build_set_of_debs_from_patterns(debs_path, package_base_name, version, maintainer, dependencies, description,
        set_basedir, patterns, post_str=None):
    """
    Maybe you have a big directory that youwant to split into several DEB files. This functions helps in that.
    """
    if not post_str:
        post_str = version.replace('.', '-')
    for (packaname, packpats) in patterns:
        modlist = []
        for packamods in packpats:
            # Build a pattern:
            fullpat = os.path.join(set_basedir, packamods+"*")
            # Shell-expand the pattern:
            alle = glob.glob(fullpat)
            modlist.extend(alle)
        # A name for the package:
        packagename = "%s-%s" % ( package_base_name, packaname, )
        debname = os.path.join( debs_path, packagename+"-"+post_str+".deb" )
        # Build the package:
        build_deb_from_files(
            debfile         = debname,
            packagename     = packagename,
            version         = version,
            maintainer      = maintainer,
            dependencies    = dependencies,
            description     = description,
            pathlist        = modlist,
            )
