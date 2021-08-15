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

##
if __name__ == '__main__':
    # main()
    pass
    ##
else:
    pass
    ##
