import os, subprocess

class AbstractPreparer:
    def __init__(self, tmpdir):
        self.tmpdir = tmpdir
    
    def prepare(self):
        raise NotImplementedError()
    def cleanup(self):
        raise NotImplementedError()

class CMMIPreparer(AbstractPreparer):
    def __init__(self, tmpdir, tarball_url, configure_parms=[]):
        super(CMMIPreparer, self).__init__(tmpdir)
        self.tarball_url = tarball_url
        self.configure_parms = configure_parms
    
    def prepare(self):
        self.get_src_tarball(self.tarball_url)
    
    def cleanup(self):
        pass
    
    def get_src_tarball(self, url):
        print("== Downloading %s . . ." % url)
        # Calculating names:
        out_filename = os.path.basename(url)
        destdir = os.path.join(self.tmpdir, 'src')
        # Creating dirs:
        subprocess.run(
            args = [ 'mkdir', '-p', destdir, ],
            check = True,
            )
        # Downloading...
        subprocess.run(
            args = [
                'wget', '-c', url,
                '-O', os.path.join(destdir, out_filename),
                ],
            check = True,
            )
