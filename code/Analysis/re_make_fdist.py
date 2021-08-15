"""docstring."""
##
import pandas as pd
from Code import ns as ns
from Code import cf as cf
import shutil


dirs = ns.Dirs()

def main():
    pass
    ##
    shutil.rmtree(dirs.FormalDist, ignore_errors=True)
    fdirs = [dirs.FormalDist, dirs.FCode, dirs.Fdata, dirs.Ffigs]
    for di in fdirs:
        di.mkdir()
    ##
    cf.copytree(dirs.Code, dirs.FCode)
    ##
    cf.copytree(dirs.out_data, dirs.Fdata)
    ##
    cf.copytree(dirs.figs, dirs.Ffigs)
    ##
    shutil.copy2(ns.CWD / 'main.py', dirs.FormalDist)
    ##
    shutil.copy2(ns.CWD / 'requirements.txt', dirs.FormalDist)

##
if __name__ == '__main__':
    # main()
    pass
    ##
else:
    pass
    ##
