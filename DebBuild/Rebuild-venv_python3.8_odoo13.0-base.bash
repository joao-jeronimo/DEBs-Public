export DEBNAME="venv-python38-odoo13-base"
source lib_build_deb.bash
echo "== Building DEB file for directory $DEBNAME . . ."

for srcdir in /odoo/VirtualEnvs/Env_Python3.8_Odoo13.0/{bin,include,pyvenv.cfg,share,lib64}
do
    rsynch_full_path "$srcdir" "$DEBNAME"/
done

dpkg-deb --build --root-owner-group "$DEBNAME"/ ../DEBs/venv-python38-odoo13-base-2023-03-2023.deb
