import subprocess, os

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
    subprocess.run(['mkdir', '-p', dstdir])
    # Rsync asked stuff:
    subprocess.run(['rsync', '-rlt', '--delete', '--itemize-changes', '-Rv', src, dst])

def build_deb_from_files(debfile, packagename, version, maintainer, dependencies, description, pathlist):
    # Mksure the dir exists:
    subprocess.run(['mkdir', '-p', packagename])
    # Copy the future package contentes theire:
    for onepath in pathlist:
        rsynch_full_path(
            src = onepath,
            dst = (packagename + os.path.sep),
            )
    # Generate the control file:
    with open( os.path.join(packagename, "DEBIAN", "control") as outcontrol:
        outcontrol.write(control_file_template % {
            'pkgname'           : packagename,
            'version'           : version,
            'dependencies'      : " ".join(dependencies),
            'arch'              : "all",
            'maintainer'        : maintainer,
            'description'       : description,
            })
    # Invoke dpkg-deb:
    subprocess.run([
        'dpkg-deb', '--build', '--root-owner-group',
        packagename, debfile, ])

############################################################################
############################################################################
############################################################################

build_deb_from_files(
    debfile         = "../DEBs/venv-python38-odoo13-base-2023-03-2023.deb",
    packagename     = "venv-python38-odoo13-base",
    version         = "2023.03.16",
    maintainer      = "João Jerónimo <joao.jeronimo.pro@gmail.com>",
    dependencies    = ["python-3.8-complete"],
    description     = "Odoo ERP, packaged for use with AutoERP.",
    pathlist        = [
        "/odoo/VirtualEnvs/Env_Python3.8_Odoo13.0/bin"
        "/odoo/VirtualEnvs/Env_Python3.8_Odoo13.0/include"
        "/odoo/VirtualEnvs/Env_Python3.8_Odoo13.0/pyvenv.cfg"
        "/odoo/VirtualEnvs/Env_Python3.8_Odoo13.0/share"
        "/odoo/VirtualEnvs/Env_Python3.8_Odoo13.0/lib64"
        ],
    )

