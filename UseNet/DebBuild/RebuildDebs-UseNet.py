#!/usr/bin/python3
import sys, os, glob, subprocess
scriptdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.join(scriptdir, os.path.pardir, os.path.pardir, "Libs")
sys.path.insert(0, parentdir)
from lib_build_deb import *

NO_REBUILD = True
NO_RETREE = False
NO_REDEB = False

############################################################################
##### InterNetNews:            #############################################
############################################################################
if not NO_REBUILD:
    mkbuilddirs()
    get_src_tarball('https://archives.eyrie.org/software/inn/inn-2.7.0.tar.gz')
    expand_src_tarball('inn-2.7.0', 'tar.gz')
    # Build dependencies:
    #apt_install_build_deps_for('inn2')
    apt_install_package(
        'build-essential', 'make', 'autoconf',
        'bison', 'flex',
        'perl',
            'libgd-perl', 'libmime-tools-perl',
        'default-mta',
        )
    # Building:
    #../../src/inn-2.7.0/configure --prefix=/UseNet/inn2 --with-perl --with-python
    configure_tarball('inn-2.7.0', '/UseNet/inn2', insource=True, configflags=['--with-perl', '--with-python'])
    build_tarball('inn-2.7.0', insource=True)

if not NO_RETREE:
    # Fake-installing:
    install_tarball('inn-2.7.0', insource=True)
if not NO_REDEB:
    # Build control file and the DEB file:
    build_deb_from_installed_files(
        debfile         = "../DEBs/usenet-inn2-2.7.0.deb",
        packagename     = "usenet-inn2",
        version         = "2.7.0",
        maintainer      = "João Jerónimo <joao@uniaolisboa-cgtp.pt>",
        dependencies    = [
            "libgd-perl",
            "libpython3.9",
            ],
        description     = "InterNetNews 2",
        pathlist = [
            '/UseNet/inn2',
            ],
        omitfiles = [
            'usenet-inn2/UseNet/inn2/etc/readers.conf',
            ],
        )
publish_files("../DEBs/usenet-inn2-2.7.0.deb", "jj@10.74.74.41",)


############################################################################
##### Systemd and config files:            #################################
############################################################################
if not NO_REDEB:
    # Build control file and the DEB file:
    build_deb(
        debfile         = "../DEBs/usenet-systemd-2.7.0.deb",
        packagename     = "usenet-systemd",
        version         = "2.7.0",
        maintainer      = "João Jerónimo <joao@uniaolisboa-cgtp.pt>",
        dependencies    = [
            "usenet-inn2",
            ],
        description     = "InterNetNews 2",
        )
publish_files("../DEBs/usenet-systemd-2.7.0.deb", "jj@10.74.74.41",)
