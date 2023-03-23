#!/usr/bin/python3
import os, glob
from lib_build_deb import *

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
        "/odoo/VirtualEnvs/Env_Python3.8_Odoo13.0/bin",
        "/odoo/VirtualEnvs/Env_Python3.8_Odoo13.0/include",
        "/odoo/VirtualEnvs/Env_Python3.8_Odoo13.0/pyvenv.cfg",
        "/odoo/VirtualEnvs/Env_Python3.8_Odoo13.0/share",
        "/odoo/VirtualEnvs/Env_Python3.8_Odoo13.0/lib64",
        ],
    )

venv_packages = [
    ('essentials', [
        '_cffi_backend.cpython', '_distutils_hack', 'cffi', 'pip', 'dateutil', 'python_dateutil',
        'python_stdnum', 'future', 'libfuturize', 'distutils', 'docutils', 'pyparsing', 'greenlet',
        'decorator', 'astor', 'attr', 'wheel', 'setuptools', 'stdnum',
        ]),
    ('tiny', [
        '__pycache__', 'cached_property', 'dot_parser', 'ldif',
        'polib', 'pysassc', 'six', 'sass', 'libsass', '_sass.cpython', 'samples',
        'pycparser', 'appdirs', 'bs4', 'libpasteurize', 'lxml', 'mock', 'past', 'pbr', 'tests',
        ]),
    ('networking', [
        'Werkzeug', 'werkzeug', 'cachetools', 'certifi', 'GitPython', 'Jinja2', 'jinja2', 'PyNaCl', 'nacl', 'cryptography', 'bcrypt', 'beautifulsoup4',
        'pymssql', 'pyserial', 'pysftp', 'odoo_client_lib', 'odoo_csv_tools', 'odoo_import_export_client', 'odoolib',
        'git', 'psycopg2', 'pyasn1',  'requests', 'serial', 'smmap',
        'unicodecsv', 'unidecode', 'Unidecode', 'urllib3', 'usb', 'pyusb', 'vatnumber', 'vobject', 'zeep', 'psutil', 'slapdtest', 'soupsieve',
        'paramiko', 'passlib', 'sqlparse', 'pytz', 'gevent',  'idna', 'isodate', 'ldap', 'python_ldap', '_ldap',
        ]),
    ('i18n', [
        'pkg_resources', 'chardet', 'Babel', 'babel', 'num2words',
        ]),
    ('media', [
        'PIL', 'Pillow', 'PyPDF2', 'Pygments', 'pygments', 'XlsxWriter', 'xlsxwriter', 'xlutils', 'xlwt', 'defusedxml',
        'docopt', 'ebaysdk', 'ezodf', 'ofxparse', 'pydot', 'xlrd', 'qrcode', 'reportlab',
        'Mako', 'mako', 'markupsafe', 'MarkupSafe',
        ]),
    ]


build_set_of_debs_from_patterns(
    debs_path           = "../DEBs/",
    package_base_name   = "venv-python38-odoo13",
    version             = "2023.03.16",
    maintainer          = "João Jerónimo <joao.jeronimo.pro@gmail.com>",
    dependencies        = ["python-3.8-complete"],
    description         = "Odoo ERP, packaged for use with AutoERP.",
    set_basedir         = os.path.join(
            os.path.sep,
            "odoo", "VirtualEnvs", "Env_Python3.8_Odoo13.0",
            "lib", "python3.8", "site-packages", ),
    patterns            = venv_packages,
    )
