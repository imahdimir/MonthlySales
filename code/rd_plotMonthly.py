"""docstring."""

import pandas as pd
import matplotlib.pyplot as plt
from Code import z_ns as ns
from Code import z_cf as cf
from Code.rc_monthlyStats import MonthlyStats


idx = pd.IndexSlice

dirs = ns.Dirs()
fc = ns.FormalCols()
ft = ns.FirmTypes()
ms = ns.MonthlyStatCols()
dcc = ns.DollarCpiCols()
cte = ns.Constants()

class PlotMonthly(MonthlyStats):
    def __init__(self, df: pd.DataFrame, dataset_name):
        super().__init__(df, dataset_name)

    def _set_months_as_x_axis(self):
        self.x_ax = self.m_df.index.unique(0).tolist()
        self.x_ax = [str(k) for k in self.x_ax]

    def _plot_sales_sum_monthly(self):
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
        fig_title = f"Sales Sum-{self.dn}"
        ax.set_title(fig_title)
        ax.grid(axis='y')
        f_n = f'sales-{self.dn}'
        fig_pnsuffless = dirs.figs / f_n
        # cf.save_fig_as_fmt(fig, fig_pnsuffless)
        cf.save_fig_as_fmt(fig, fig_pnsuffless, fmt='png')
        # fig.show()
        return fig

    def _plot_stack_bar(self, col_l0, col_l1, y_lbl, title):
        col0 = col_l0
        col1 = col_l1
        x = self.x_ax

        yl0 = self.m_df.loc[idx[:, ft.Production], (col0, col1)]
        yl0_lbl = ft.Production
        yl1 = self.m_df.loc[idx[:, ft.Service], (col0, col1)]
        yl1_lbl = ft.Service

        width = 0.35
        ax_y_lbl = y_lbl
        ax_x_lbl = fc.JMonth

        fig, ax = plt.subplots(figsize=(28.8, 18))

        ax.bar(x, yl0, width, label=yl0_lbl)
        ax.bar(x, yl1, width, bottom=yl0, label=yl1_lbl)

        ax.set_ylabel(ax_y_lbl)
        ax.set_xlabel(ax_x_lbl)

        ax.set_xticklabels(x, rotation=30)
        ax.legend()
        fig_n = f"{title}-{self.dn}"
        ax.set_title(fig_n)
        ax.grid(axis='y')
        fig_pnsuffless = dirs.figs / fig_n
        # cf.save_fig_as_fmt(fig, fig_pnsuffless)
        cf.save_fig_as_fmt(fig, fig_pnsuffless, fmt='png')
        return fig

    def _plot_firms_count(self):
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
        fig_n = f"FirmsCount-{self.dn}"
        ax.set_title(fig_n)
        ax.grid(axis='y')
        fig_pnsuffless = dirs.figs / fig_n
        cf.save_fig_as_fmt(fig, fig_pnsuffless)
        cf.save_fig_as_fmt(fig, fig_pnsuffless, fmt='png')
        return fig

    def build_all_plots(self):
        self.build_monthly_data()
        self._set_months_as_x_axis()

        self._plot_firms_count()
        self._plot_sales_sum_monthly()

        chart_data = [(ms.rev_Hemmat, 'mean', ms.rev_Hemmat, "MeanSales"),
                      (ms.rev_d, 'sum', ms.rev_d, ms.rev_d),
                      (ms.rev_r, 'sum', ms.rev_r, ms.rev_r),
                      ("", ms.norm_rev, "", ms.norm_rev),
                      ("", ms.norm_rev_d, "", ms.norm_rev_d),
                      ("", ms.norm_rev_r, "", ms.norm_rev_r)]
        for ch in chart_data:
            self._plot_stack_bar(col_l0=ch[0],
                                 col_l1=ch[1],
                                 y_lbl=ch[2],
                                 title=ch[3])

def main():
    pass
    ##
    ws = cf.load_whole_sample()
    bs = cf.load_balanced_subsample()

    data = {cte.Whole   : ws,
            cte.Balanced: bs}

    for ke, va in data.items():
        ms_o = PlotMonthly(va, ke)
        ms_o.build_all_plots()

##
if __name__ == '__main__':
    main()
    print(f'{__file__} Done.')
    pass
else:
    pass
    ##
