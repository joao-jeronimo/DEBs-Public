
# Python:
mkdir -p Python-3.8.15-Odoo-Complete/odoo/RunTime/
cp -Rv /odoo/RunTime/Python-3.8-install/ Python-3.8.15-Odoo-Complete/odoo/RunTime/
dpkg-deb --build --root-owner-group Python-3.8.15-Odoo-Complete/

# Odoo13:
mkdir -p Odoo13/odoo/releases/13.0/
cp -Rv /odoo/releases/13.0/.git Odoo13/odoo/releases/13.0/
dpkg-deb --build --root-owner-group Odoo13/
