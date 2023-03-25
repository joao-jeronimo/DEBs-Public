#!/usr/bin/python3
import os, glob, subprocess
from lib_build_deb import *

NO_REBUILD = True
NO_REDEB = True

if not NO_REBUILD:
    ############################################################################
    ############################################################################
    ############################################################################
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

if not NO_REDEB:
    # Fake-installing:
    install_tarball('inn-2.7.0', 'Usenet-inn2/', insource=True)
    # Build control file and the DEB file:
    build_deb(
        debfile         = "../DEBs/Usenet-inn2-2.7.0.deb",
        packagename     = "Usenet-inn2",
        version         = "2.7.0",
        maintainer      = "João Jerónimo <joao@uniaolisboa-cgtp.pt>",
        dependencies    = [
            "libgd-perl",
            ],
        description     = "InterNetNews 2",
        )
publish_files("../DEBs/Usenet-inn2-2.7.0.deb", "jj@10.74.74.41",)
