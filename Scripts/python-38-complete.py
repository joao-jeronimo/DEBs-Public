import deb_building_lib

class Prepare1(deb_building_lib.preparers.CMMIPreparer):
    def __init__(self, tmpdir):
        super(Prepare1, self).__init__(
            tmpdir          = tmpdir,
            tarball_url     = "https://www.python.org/ftp/python/3.8.17/Python-3.8.17.tar.xz",
            configure_parms = [ "--enable-optimizations", ],
            )
