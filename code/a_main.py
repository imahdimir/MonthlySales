""" python v. == 3.6.13 only
    install pkgs in requirements.txt
    This Script only updates the sale data to the latest data available on Codal.ir
    set the Code folder PARENT dir as Current Working Direcoty(cwd) to code can be run
    """
##
import importlib
from Code import z_cf as cf
from Code import z_ns as ns


dirs = ns.Dirs()
pa = ns.BalancedSubsampleConfig()
vif = ns.VeryImportantFiles()

pa.initJMonth = 139601
pa.lastJMonth = None

self_n = 'a_main'
self_pn = dirs.Code / f'{self_n}.py'

print(self_pn)
pys = cf.load_pns_of_all_modules_in_the_same_dir_except(self_pn)
print(pys)

def main():
    pass
    ##
    dct = {}
    for mod in pys:
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
