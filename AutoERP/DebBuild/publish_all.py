#!/usr/bin/python3
import sys, os, glob, subprocess
scriptdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.join(scriptdir, os.path.pardir, os.path.pardir, "Libs")
sys.path.insert(0, parentdir)
from lib_build_deb import *

for filenm in os.listdir('../DEBs/'):
    fpath = os.path.join("../DEBs", filenm)
    publish_files(fpath, "jj@10.74.74.41",)
