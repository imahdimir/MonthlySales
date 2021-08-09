""""""

##
import pandas as pd

from py import z_ns as ns
from ReportMaker.py import r_z_cf as rcf
from ReportMaker.py import r_a_main as rm


imf = ns.ImportantFiles()
pdirs = ns.ProjectDirectories()
fc = ns.FormalCols()

def main():
    pass
    ##
    with open(imf.lastData, 'r') as f:
        lad_n = f.read()

    lad_pn = pdirs.output / lad_n
    dta = pd.read_excel(lad_pn, engine = 'openpyxl')
    ##
    c_dta = dta[dta[fc.JMonth].ge(rm.pa.start_jmonth)]
    if rm.end_jmonth is not None:
        c_dta = c_dta[c_dta[fc.JMonth].le(rm.pa.end_jmonth)]

    b_dta = rcf.make_balanced_subsample(c_dta,
                                        col2balance_across = fc.JMonth,
                                        target_column = fc.Ticker)

##
if __name__ == '__main__':
    pass
else:
    pass
    ##
