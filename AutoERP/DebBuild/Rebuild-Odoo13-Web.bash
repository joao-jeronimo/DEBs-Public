export DEBNAME="Odoo13-Web"
source lib_build_deb.bash
echo "== Building DEB file for directory $DEBNAME . . ."

for srcdir in /odoo/releases/13.0/addons/web*
do
    rsynch_full_path "$srcdir" "$DEBNAME"/
done

dpkg-deb --build --root-owner-group "$DEBNAME"/ ../DEBs/Odoo13-Web-2023.01.11.deb
