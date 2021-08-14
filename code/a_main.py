""" python v. == 3.6.13 only
    install pkgs in requirements.txt
    This Script only updates the sale data to the latest data available on Codal.ir
    set the Code folder PARENT dir as Current Working Direcoty(cwd) to code can be run
    """
##
from pathlib import Path
import importlib
from Code import z_cf as cf
from Code import z_ns as ns


CWD = Path.cwd()
dirs = ns.Dirs()

pa = ns.Params()
pa.initial_jmonth = 139601
pa.last_jmonth = None


def main():
    pass
    ##
    dct = {}
    ms2load = cf.load_modules_pths(dirs.Code)
    for mod in ms2load:
        dct[str(mod)] = importlib.import_module(mod, package=None)
    print(dct)
    ##
    for v in dct.values():
        v.main()


##
if __name__ == "__main__":
    main()
    print(f'All Done! \n The Monthly Sale Data is Updated. The associated Excel file is in the output folder.')
else:
    pass
    ##
