export DEBNAME="Odoo13-Account"
source lib_build_deb.bash
echo "== Building DEB file for directory $DEBNAME . . ."

for srcdir in /odoo/releases/13.0/addons/account*
do
    rsynch_full_path "$srcdir" "$DEBNAME"/"$srcdir"
done

dpkg-deb --build --root-owner-group "$DEBNAME"/ ../DEBs/Odoo13-Account-2023.01.11.deb
