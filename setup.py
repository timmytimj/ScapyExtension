#! /usr/bin/env python


from distutils import archive_util
from distutils import sysconfig
#from distutils.core import setup
from setuptools import setup, find_packages
from distutils.command.sdist import sdist
import os
from scapy.config import conf

EZIP_HEADER="""#! /bin/sh
PYTHONPATH=$0/%s exec python -m scapy.__init__
"""

def make_ezipfile(base_name, base_dir, verbose=0, dry_run=0):
    fname = archive_util.make_zipfile(base_name, base_dir, verbose, dry_run)
    ofname = fname+".old"
    os.rename(fname,ofname)
    of=open(ofname)
    f=open(fname,"w")
    f.write(EZIP_HEADER % base_dir)
    while True:
        data = of.read(8192)
        if not data:
            break
        f.write(data)
    f.close()
    of.close()
    os.unlink(ofname)
    os.chmod(fname,0755)
    return fname



archive_util.ARCHIVE_FORMATS["ezip"] = (make_ezipfile,[],'Executable ZIP file')

SCRIPTS = ['bin/scapy','bin/UTscapy']
# On Windows we also need additional batch files to run the above scripts 
if os.name == "nt":
  SCRIPTS += ['bin/scapy.bat','bin/UTscapy.bat']

setup(
    name = 'scapy',
    #version = '2.1.1CX_build20110505',
    version = conf.version,
    packages=['scapy','scapy/arch', 'scapy/arch/windows', 'scapy/layers','scapy/asn1','scapy/tools','scapy/modules', 'scapy/crypto'],
    scripts = SCRIPTS,
    data_files = [('share/man/man1', ["doc/scapy.1.gz"])],

    # Metadata
    author = 'Philippe BIONDI',
    author_email = 'phil(at)secdev.org',
    description = 'Scapy: interactive packet manipulation tool',
    license = 'GPLv2',
    zip_safe=False ,
    url = 'http://www.secdev.org/projects/scapy'
    # keywords = '',
    # url = '',
)
