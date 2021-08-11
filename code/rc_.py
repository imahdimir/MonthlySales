"""docstring."""

##
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from py import z_ns as ns
from ReportMaker.py import r_z_cf as rcf
from ReportMaker.py import r_z_ns as rns
from py import z_cf as cf


idx = pd.IndexSlice

fc = ns.FormalCols()
ft = ns.FirmTypes()
ms = rns.MonthlyStatCols()
ds = rns.DataSetsNames()
rdirs = rns.FormalReportDirectories()


class MonthlyStats:
    def __init__(self, df: pd.DataFrame, dataset_name):
        """ds."""

        self.dn = dataset_name
        self.df = df

        self.monthly_group_by = [fc.JMonth, fc.FirmType]
        self.m_df = None

        self.x_ax = None


    def build_monthly_data(self):
        self.df = self.df.sort_values(fc.JMonth)
        self.df[ms.rev_Hemmat] = self.df[fc.RevenueBT] / 10 ** 3
        self.df = self.df.drop(columns=fc.RevenueBT)

        mo_multi_ind = pd.MultiIndex.from_product([self.df[fc.JMonth].unique(),
                                                   self.df[
                                                       fc.FirmType].unique()],
                                                  names=self.monthly_group_by)
        self.m_df = pd.DataFrame(index=mo_multi_ind)
        grouped = self.df.groupby(self.monthly_group_by)
        dsc = grouped.describe().round(3)
        self.m_df = self.m_df.join(dsc)

        sdf = grouped.sum()
        sdf.columns = [(ms.rev_Hemmat, 'sum')]
        self.m_df = self.m_df.join(sdf)
        m_df_cmi = pd.MultiIndex.from_tuples(self.m_df.columns.tolist())
        self.m_df = self.m_df.reindex(m_df_cmi, axis=1)
        cf.save_df_to_xl(self.m_df,
                         rdirs.data / f"Monthly-{self.dn}",
                         index=True,
                         float_format="%.3f")

        self.x_ax = self.m_df.index.unique(0).tolist()
        self.x_ax = [str(k) for k in self.x_ax]


    def plot_sales_sum_monthly(self):
        """"""
        x = self.x_ax
        yl0 = self.m_df.loc[
            idx[:, ft.Production], (ms.rev_Hemmat, 'sum')]
        yl0_lbl = ft.Production
        yl0err = self.m_df.loc[
            idx[:, ft.Production], (ms.rev_Hemmat, 'std')]
        yl1 = self.m_df.loc[
            idx[:, ft.Service], (ms.rev_Hemmat, 'sum')]
        yl1_lbl = ft.Service
        yl1err = self.m_df.loc[
            idx[:, ft.Service], (ms.rev_Hemmat, 'std')]

        width = 0.35
        ax_y_lbl = ms.rev_Hemmat
        ax_x_lbl = fc.JMonth

        fig, ax = plt.subplots(figsize=(28.8, 18))

        ax.bar(x, yl0, width, yerr=yl0err, label=yl0_lbl)
        ax.bar(x, yl1, width, yerr=yl1err, bottom=yl0, label=yl1_lbl)

        ax.set_ylabel(ax_y_lbl)
        ax.set_xlabel(ax_x_lbl)

        ax.set_xticklabels(x, rotation=30)
        ax.legend()
        fig_n = f"Sales Sum-{self.dn}"
        ax.set_title(fig_n)
        ax.grid(axis='y')
        fig_pnsuffless = rdirs.figs / fig_n
        save_fig_as_fmt(fig, fig_pnsuffless)
        fig.show()
        return fig


    def plot_sales_mean_monthly(self):
        x = self.x_ax
        yl0 = self.m_df.loc[
            idx[:, ft.Production], (ms.rev_Hemmat, 'mean')]
        yl0_lbl = ft.Production
        yl1 = self.m_df.loc[
            idx[:, ft.Service], (ms.rev_Hemmat, 'mean')]
        yl1_lbl = ft.Service

        width = 0.35
        ax_y_lbl = ms.mean_rev_ht
        ax_x_lbl = fc.JMonth

        fig, ax = plt.subplots(figsize=(28.8, 18))

        ax.bar(x, yl0, width, label=yl0_lbl)
        ax.bar(x, yl1, width, bottom=yl0, label=yl1_lbl)

        ax.set_ylabel(ax_y_lbl)
        ax.set_xlabel(ax_x_lbl)

        ax.set_xticklabels(x, rotation=30)
        ax.legend()
        fig_n = f"Sales Mean-{self.dn}"
        ax.set_title(fig_n)
        ax.grid(axis='y')
        fig_pnsuffless = rdirs.figs / fig_n
        save_fig_as_fmt(fig, fig_pnsuffless)
        return fig


    def plot_firms_count(self):
        x = self.x_ax
        yl0 = self.m_df.loc[
            idx[:, ft.Production], (ms.rev_Hemmat, 'count')]
        yl0_lbl = ft.Production
        yl1 = self.m_df.loc[
            idx[:, ft.Service], (ms.rev_Hemmat, 'count')]
        yl1_lbl = ft.Service

        width = 0.35
        ax_y_lbl = 'count'
        ax_x_lbl = fc.JMonth

        fig, ax = plt.subplots(figsize=(28.8, 18))

        ax.bar(x, yl0, width, label=yl0_lbl)
        ax.bar(x, yl1, width, bottom=yl0, label=yl1_lbl)

        ax.set_ylabel(ax_y_lbl)
        ax.set_xlabel(ax_x_lbl)

        ax.set_xticklabels(x, rotation=30)
        ax.legend()
        fig_n = f"Firms Count-{self.dn}"
        ax.set_title(fig_n)
        ax.grid(axis='y')
        fig_pnsuffless = rdirs.figs / fig_n
        save_fig_as_fmt(fig, fig_pnsuffless)
        return fig


    def plot_all(self):
        self.build_monthly_data()
        self.plot_sales_sum_monthly()
        self.plot_sales_mean_monthly()
        if self.dn == ds.whole_sample:
            self.plot_firms_count()
        else:


def save_fig_as_fmt(fig, pn_suffless, fmt='eps'):
    fig.savefig(f'{pn_suffless}.{fmt}', format=fmt, dpi=1200)


def main():
    pass
    ##
    ws = rcf.load_whole_sample()
    bs = rcf.load_balanced_subsample()

    ws_lbl = ds.whole_sample
    bs_lbl = ds.balanced_subsample

    data_dct = {ws_lbl: ws,
                bs_lbl: bs}
    for ke, va in data_dct.items():
        dgo = MonthlyStats(va, ke)
        dgo.plot_all()

    ##


##
if __name__ == '__main__':
    pass
else:
    pass
    ##
