
# Odoo13:
mkdir -p Odoo13/odoo/releases/13.0/
cp -Rv /odoo/releases/13.0/.git Odoo13/odoo/releases/13.0/
dpkg-deb --build --root-owner-group Odoo13/
