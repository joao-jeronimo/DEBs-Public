#!/usr/bin/python3
import os, glob
from lib_build_deb import *

############################################################################
############################################################################
############################################################################

build_deb_from_files(
    debfile         = "../DEBs/sidil13-installer-2023-03-23.deb",
    packagename     = "sidil13-installer",
    version         = "2023.03.23",
    maintainer      = "João Jerónimo <joao@uniaolisboa-cgtp.pt>",
    dependencies    = [
        "venv-python38-odoo13-base",
        "venv-python38-odoo13-essentials",
        "venv-python38-odoo13-i18n",
        "venv-python38-odoo13-media",
        "venv-python38-odoo13-networking",
        "venv-python38-odoo13-tiny",
        ],
    description     = "Instalador do SIDIL.",
    pathlist        = [
        "/odoo/sidilcode13/SIDIL-Installer/.git",
        ],
    )
