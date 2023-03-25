#!/usr/bin/python3
import os, glob
from lib_build_deb import *

############################################################################
############################################################################
############################################################################
mkdir -p ../builds/
wget -c https://archives.eyrie.org/software/inn/inn-2.7.0.tar.gz -O ../builds/

exit 0
build_deb_from_files(
    debfile         = "../DEBs/Usenet-inn2-2.7.0.deb",
    packagename     = "Usenet-inn2",
    version         = "2.7.0",
    maintainer      = "João Jerónimo <joao@uniaolisboa-cgtp.pt>",
    dependencies    = [
        #"venv-python38-odoo13-base",
        ],
    description     = "InterNetNews 2",
    pathlist        = [
        "/UseNet/inn2",
        ],
    )
