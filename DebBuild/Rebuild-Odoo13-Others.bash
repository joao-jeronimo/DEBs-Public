export DEBNAME="Odoo13-Others"
source lib_build_deb.bash
echo "== Building DEB file for directory $DEBNAME . . ."

for srcdir in   /odoo/releases/13.0/addons/analytic*                    \
                /odoo/releases/13.0/addons/association*                 \
                /odoo/releases/13.0/addons/attachment_indexation*       \
                /odoo/releases/13.0/addons/auth*                        \
                /odoo/releases/13.0/addons/[bcdefghijklmnopqrstuv]*     \
                /odoo/releases/13.0/addons/[xyz]*
do
    rsynch_full_path "$srcdir" "$DEBNAME"/"$srcdir"
done

dpkg-deb --build --root-owner-group "$DEBNAME"/ ../DEBs/Odoo13-Others-2023.01.11.deb
