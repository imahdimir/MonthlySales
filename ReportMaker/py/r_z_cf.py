""" sth """
##
import os
import shutil
import pandas as pd
from py import z_ns as ns
from ReportMaker.py import r_a_main as rm
from ReportMaker.py import r_z_ns as rns
from py import z_cf as cf


dirs = ns.ProjectDirectories()
imf = ns.ImportantFiles()

rdfn = rns.DataFilesNames()
rdirs = rns.FormalReportDirectories()

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def make_balanced_subsample(df: pd.DataFrame,
                            col2balance_across: str,
                            target_column: str):
    """ Makes the balanced subsample of df across col2balance, it finds all target values that have at least one observation for each value of col2balance
        Returns the common target values
        """

    x = col2balance_across
    y = target_column

    common_y = set(df[y].unique())

    for _, gp in df.groupby([x]).__iter__():
        common_y &= set(gp[y].unique())

    bs = df[df[y].isin(common_y)]
    return bs

def load_whole_sample():
    """return latest whole sample"""

    with open(imf.lastData, 'r') as f:
        xln = f.read()

    xl_pn = dirs.output / xln
    df = pd.read_excel(xl_pn, engine = 'openpyxl')
    return df

def load_balanced_subsample():
    """sth"""
    bs_n_pn = rdirs.data / f'{rdfn.bs_name_txt}.txt'
    with open(bs_n_pn, 'r') as f:
        bs_pn = f.read()
    return pd.read_excel(bs_pn, engine = 'openpyxl')
