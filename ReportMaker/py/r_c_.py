"""docstring."""

##
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from py import z_ns as ns
from ReportMaker.py import r_z_cf as rcf
from ReportMaker.py import r_z_ns as rns


fc = ns.FormalCols()
ft = ns.FirmTypes()

class DataGraphs:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.df = self.df.sort_values(fc.JMonth)

        self.monthly_stat = None
        self.monthly_group_by = [fc.JMonth, fc.FirmType]
        grouped = self.df.groupby(self.monthly_group_by)
        self.monthly_stat = grouped.describe().round(3)

    def plt_sales_sum_monthly(self):
        """"""
        grouped = self.df.groupby(self.monthly_group_by)
        sdf = grouped.sum()
        self.monthly_stat = self.monthly_stat.join(sdf)

        x = self.monthly_stat.index
        yl0 = self.monthly_stat.loc[(, ft.Production), (fc.RevenueBT, 'sum')]
        yl1 = self.monthly_stat.loc[]

        ax = plt.subplot()
        ax.b

def main():
    pass
    ##
    ws = rcf.load_whole_sample()
    bs = rcf.load_balanced_subsample()
    ##
    grph = DataGraphs(ws)
    tdf = grph.monthly_stat

##
if __name__ == '__main__':
    pass
else:
    pass
    ##
