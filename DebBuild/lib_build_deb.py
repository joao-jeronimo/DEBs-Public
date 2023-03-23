import subprocess, os, glob

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
