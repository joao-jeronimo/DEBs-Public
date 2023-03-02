
# Python:
mkdir -p Python-3.8.15-Odoo-Complete/odoo/RunTime/
rsync -rlt --delete --itemize-changes                       \
    /odoo/RunTime/Python-3.8-install/                       \
    Python-3.8.15-Odoo-Complete/odoo/RunTime/
dpkg-deb --build --root-owner-group Python-3.8.15-Odoo-Complete/
