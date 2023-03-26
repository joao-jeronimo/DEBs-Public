#!/usr/bin/python3
import sys, os, glob
scriptdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.join(scriptdir, os.path.pardir, os.path.pardir, "Libs")
sys.path.insert(0, parentdir)
from lib_build_deb import *

############################################################################
############################################################################
############################################################################

build_deb_from_installed_files(
    debfile         = "../DEBs/sidil13-installer-2023-03-23.deb",
    packagename     = "sidil13-installer",
    version         = "2023.03.23",
    maintainer      = "João Jerónimo <joao@uniaolisboa-cgtp.pt>",
    dependencies = [
        "sudo", "git", "screenie",
        "venv-python38-odoo13-base", "venv-python38-odoo13-essentials", "venv-python38-odoo13-i18n", "venv-python38-odoo13-media", "venv-python38-odoo13-networking", "venv-python38-odoo13-tiny",
        "gpg", "lsb-release", "locate", "software-properties-common", "make", "gmsl", "nginx", "resolvconf",
        "libffi-dev", "libsasl2-dev", "libldap2-dev", "libssl-dev", "libpq-dev", "libjpeg-dev", "libxml2-dev", "libxslt-dev", "zlib1g-dev",
        "postgresql", "postgresql-client", "postgresql-contrib",
        "ttf-mscorefonts-installer", "fonts-lato", "node-less", "rustc", "libncurses-dev",
        ],
    description     = "Instalador do SIDIL.",
    pathlist = [
        "/odoo/sidilcode13/SIDIL-Installer/.git",
        ],
    omitfiles = [
        ],
    )

build_deb(
    debfile         = "../DEBs/sidil13-tools-2023-03-23.deb",
    packagename     = "sidil13-tools",
    version         = "2023.03.23",
    maintainer      = "João Jerónimo <joao@uniaolisboa-cgtp.pt>",
    dependencies    = [
        "sidil13-installer",
        ],
    description     = "Ferramentas do SIDIL no Nginx default.",
    )
