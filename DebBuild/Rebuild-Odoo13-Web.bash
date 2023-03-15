export DEBNAME="Odoo13-Web"
source lib_build_deb.bash
echo "== Building DEB file for directory $DEBNAME . . ."

rsynch_full_path /odoo/releases/13.0/odoo/addons/web*   "$DEBNAME"/odoo/releases/13.0/

dpkg-deb --build --root-owner-group "$DEBNAME"/ ../DEBs/Odoo13-Web-2023.01.11.deb
