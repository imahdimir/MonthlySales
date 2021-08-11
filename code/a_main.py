""" python v. == 3.6.13 only
    install pkgs in requirements.txt
    This Script only updates the sale data to the latest data available on Codal.ir
    set the Code folder PARENT dir as Current Working Direcoty(cwd) to code can be run
    """
##
from pathlib import Path
import importlib
from Code import z_cf as cf


CWD = Path.cwd()


class Params:
    def __init__(self,
                 initial_jmonth_4balanced_subsample=139601,
                 last_jmonth=None):
        self.initial_jmoneh = initial_jmonth_4balanced_subsample
        self.last_jmonth = last_jmonth
        self.py_code_dir_n = 'Code'


pa = Params()
py_dir = CWD / pa.py_code_dir_n


def main():
    pass
    ##
    dct = {}
    ms2load = cf.load_modules_pths(py_dir)
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
