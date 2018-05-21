#pylint: disable=no-name-in-module,import-error
from distutils.command.install_headers import install_headers
import os

# TODO: Change to pathlib
class InstallHeaders(install_headers):
    '''install_headers by default flattens subdirectories'''
    def run (self):
        if not self.distribution.headers: return
        for header in self.distribution.headers:
            subdir = os.path.dirname(header)
            install_dir = os.path.join(self.install_dir, subdir)
            self.mkpath(install_dir)
            out, _ = self.copy_file(header, install_dir)
            self.outfiles.append(out)