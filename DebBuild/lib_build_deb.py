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
            'dependencies'      : " ".join(dependencies),
            'arch'              : "all",
            'maintainer'        : maintainer,
            'description'       : description,
            })
    # Invoke dpkg-deb:
    subprocess.check_call([
        'dpkg-deb', '--build', '--root-owner-group',
        packagename, debfile, ])
