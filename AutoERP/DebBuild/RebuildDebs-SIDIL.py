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
        "git",
        "venv-python38-odoo13-base", "venv-python38-odoo13-essentials", "venv-python38-odoo13-i18n", "venv-python38-odoo13-media", "venv-python38-odoo13-networking", "venv-python38-odoo13-tiny",
        "gpg", "lsb-release", "locate", "software-properties-common", "make", "gmsl", "nginx", "resolvconf",
        "libffi-dev", "libsasl2-dev", "libldap2-dev", "libssl-dev", "libpq-dev", "libjpeg-dev", "libxml2-dev", "libxslt-dev", "zlib1g-dev",
        "postgresql", "postgresql-client", "postgresql-contrib",
        "ttf-mscorefonts-installer", "fonts-lato", "node-less", "rustc", "libncurses-dev"
        ],
    description     = "Instalador do SIDIL.",
    pathlist        = [
        "/odoo/sidilcode13/SIDIL-Installer/.git",
        ],
    )
