"""doc."""

##
from pathlib import Path
import shutil
from py import z_ns as ns
from ReportMaker.py import r_z_ns as rns
from ReportMaker.py import r_z_cf as rcf


mfd = ns.MandatoryDirsFiles()
fr = rns.FormalReportDirectories()
imf = ns.ImportantFiles()
pdirs = ns.ProjectDirectories()
pa = rns.Parameters()

pa.start_jmonth = 139601
pa.end_jmonth = None

def main():
    pass
    ##
    shutil.rmtree(fr.dirpath, ignore_errors = True)

    fr.dirpath.mkdir()
    fr.code.mkdir()
    fr.raw.mkdir()
    fr.figs.mkdir()
    fr.data.mkdir()

    rcf.copytree(mfd.py, fr.code)
    rcf.copytree(mfd.raw, fr.raw)

    # with open(imf.lastData, 'r') as f:
    #     lad_n = f.read()
    #
    # lad_pn = pdirs.output / lad_n
    # shutil.copy2(lad_pn, fr.dirpath)

##
if __name__ == "__main__":
    main()
else:
    pass
    ##
