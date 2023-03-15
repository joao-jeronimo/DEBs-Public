export DEBNAME="Odoo13-Core"
source lib_build_deb.bash
echo "== Building DEB file for directory $DEBNAME . . ."
rsynch_full_path /odoo/releases/13.0/odoo/ "$DEBNAME"/odoo/releases/13.0/
dpkg-deb --build --root-owner-group "$DEBNAME"/
