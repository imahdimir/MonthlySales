"""docstring."""

##
import pandas as pd
from Code import ns as ns
from Code import cf as cf
import math


idx = pd.IndexSlice

dirs = ns.Dirs()
fc = ns.FormalCols()
ft = ns.FirmTypes()
ms = ns.MonthlyStatCols()
dcc = ns.DollarCpiCols()
cte = ns.Constants()

class MonthlyStats:
    def __init__(self, df: pd.DataFrame, dataset_name):
        """ds."""
        self.dn = dataset_name
        self.df = df
        self.monthly_group_by = [fc.JMonth, fc.FirmType]
        self.m_df = None
        self.x_ax = None
        self.base_yr_vals = None

    def _convert_bt2hemmat(self):
        self.df = self.df.sort_values(fc.JMonth)
        self.df[ms.rev_Hemmat] = self.df[fc.RevenueBT] / 10 ** 3
        self.df = self.df.drop(columns=fc.RevenueBT)

    def _build_monthly_description(self):
        mo_multi_ind = pd.MultiIndex.from_product([self.df[fc.JMonth].unique(),
                                                   self.df[
                                                       fc.FirmType].unique()],
                                                  names=self.monthly_group_by)
        self.m_df = pd.DataFrame(index=mo_multi_ind)
        grouped = self.df.groupby(self.monthly_group_by)
        dsc = grouped.describe().round(3)
        self.m_df = self.m_df.join(dsc)

    def _add_sum_col2monthly_stats(self):
        grouped = self.df.groupby(self.monthly_group_by)
        sdf = grouped.sum()
        sdf.columns = [(ms.rev_Hemmat, 'sum')]
        self.m_df = self.m_df.join(sdf)
        self._make_cols_multi_index()

    def _make_cols_multi_index(self):
        m_df_cmi = pd.MultiIndex.from_tuples(self.m_df.columns.tolist())
        self.m_df = self.m_df.reindex(m_df_cmi, axis=1)

    def _add_dollar_cpi_data_2monthly_stats(self):
        dc = cf.load_dollar_cpi()
        self.m_df = self.m_df.join(dc, on=fc.JMonth)
        self.m_df = self.m_df.rename(columns={
                dcc.Dollar: ("", dcc.Dollar),
                dcc.CPI   : ("", dcc.CPI)})
        self._make_cols_multi_index()

    def _normalize_cpi(self):
        frst_month_cpi = self.m_df.iloc[0][("", dcc.CPI)]
        self.m_df[("", ms.normed_cpi)] = self.m_df[
                                             ("", dcc.CPI)] / frst_month_cpi

    def _cal_rev_in_real_dollar(self):
        self.m_df[(ms.rev_d, 'sum')] = self.m_df[(
                ms.rev_Hemmat, 'sum')] * 10 ** 3 / self.m_df[("", dcc.Dollar)]
        self.m_df[(ms.rev_r, 'sum')] = self.m_df[(
                ms.rev_Hemmat, 'sum')] / self.m_df[("", ms.normed_cpi)]

    def _find_base_yr_vals_4normalization(self):
        cols = [ms.rev_Hemmat, ms.rev_d, ms.rev_r]
        mui_cols = [(x, 'sum') for x in cols]
        self.base_yr_vals = self.m_df.iloc[:12 * 2][mui_cols]
        self.base_yr_vals = self.base_yr_vals.rename(columns=lambda x: 'byr_sum',
                                                     level=1)
        append_times = math.floor(len(self.m_df) / 2 / 12)
        helper_df = self.base_yr_vals
        for _ in range(0, append_times):
            self.base_yr_vals = self.base_yr_vals.append(helper_df)
        self.base_yr_vals = self.base_yr_vals.iloc[:len(self.m_df)]
        self.base_yr_vals = self.base_yr_vals.set_index(self.m_df.index)
        self.m_df = self.m_df.join(self.base_yr_vals)
        return self.m_df

    def _normalize_with_respect_to_base_yr(self):
        nco = [ms.norm_rev, ms.norm_rev_d, ms.norm_rev_r]
        nume = [ms.rev_Hemmat, ms.rev_d, ms.rev_r]
        for ncol, nume in zip(nco, nume):
            self.m_df[("", ncol)] = self.m_df[(nume, 'sum')] / \
                                    self.m_df[(nume, 'byr_sum')]

    def build_monthly_data(self):
        self._convert_bt2hemmat()
        self._build_monthly_description()
        self._add_sum_col2monthly_stats()
        self._add_dollar_cpi_data_2monthly_stats()
        self._normalize_cpi()
        self._cal_rev_in_real_dollar()
        self._find_base_yr_vals_4normalization()
        self._make_cols_multi_index()
        self._normalize_with_respect_to_base_yr()
        cf.save_df_to_xl(self.m_df,
                         dirs.out_data / f"Monthly-{self.dn}",
                         index=True,
                         float_format="%.3f")
        return self.m_df

def main():
    pass
    ##
    ws = cf.load_whole_sample()
    bs = cf.load_balanced_subsample()

    data = {cte.Whole   : ws,
            cte.Balanced: bs}

    for ke, va in data.items():
        ms_o = MonthlyStats(va, ke)
        tdf = ms_o.build_monthly_data()
        print(tdf)

##
if __name__ == '__main__':
    main()
    print(f'{__file__} Done.')
    pass
else:
    pass
    ##
