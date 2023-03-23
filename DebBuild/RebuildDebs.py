#!/usr/bin/python3
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

for (packaname, packpats) in venv_packages:
    modlist = []
    for packamods in packpats:
        # Build a pattern:
        fullpat = os.path.join(os.path.sep,
            "odoo", "VirtualEnvs",
            "Env_Python3.8_Odoo13.0", "lib",
            "python3.8", "site-packages", packamods+"*",
            )
        # Shell-expand the pattern:
        alle = glob.glob(fullpat)
        modlist.extend(alle)
    # A name for the package:
    packagename = "venv-python38-odoo13-%s" % packaname
    # Build the package:
    build_deb_from_files(
        debfile         = "../DEBs/"+packagename+"-2023-03.16.deb",
        packagename     = packagename,
        version         = "2023.03.16",
        maintainer      = "João Jerónimo <joao.jeronimo.pro@gmail.com>",
        dependencies    = ["python-3.8-complete"],
        description     = "Odoo ERP, packaged for use with AutoERP.",
        pathlist        = modlist,
        )
