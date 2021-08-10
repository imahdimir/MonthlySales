""""""

##
import pandas as pd

from py import z_ns as ns
from ReportMaker.py import r_z_cf as rcf
from ReportMaker.py import r_a_main as rm
from ReportMaker.py import r_z_ns as rns
from py import z_cf as cf


imf = ns.ImportantFiles()
pdirs = ns.ProjectDirectories()
fc = ns.FormalCols()
dfn = rns.DataFilesNames()
ds = rns.DataSetsNames()
dd = rns.DataDescriptionCols()
ft = ns.FirmTypes()
rdirs = rns.FormalReportDirectories()

class DataDsc:
    def __init__(self, df: pd.DataFrame, the_index_lbl: str):
        self.df = df
        self.index_lbl = the_index_lbl
        self.odf = pd.DataFrame(index = [the_index_lbl])

    @property
    def init_jmonth(self):
        return self.df[fc.JMonth].min()

    @property
    def final_jmonth(self):
        return self.df[fc.JMonth].max()

    @property
    def month_count(self):
        return self.df[fc.JMonth].unique().size

    @property
    def tickers_count(self):
        return self.df[fc.Ticker].unique().size

    @property
    def production_firms_count(self):
        return self.df[self.df[fc.FirmType].eq(ft.Production)][
            fc.Ticker].unique().size

    @property
    def productions_firms_pct(self):
        return self.production_firms_count / self.tickers_count

    @property
    def obs(self):
        return self.df.shape[0]

    @property
    def avg_obs_monthly(self):
        return self.obs / self.month_count

    def ret_odf(self):
        od = self.odf
        col_val = {
                dd.obs                   : self.obs,
                dd.initial_jmonth        : self.init_jmonth,
                dd.final_jmonth          : self.final_jmonth,
                dd.month_count           : self.month_count,
                dd.avg_obs_monthly       : self.avg_obs_monthly,
                dd.firms_count           : self.tickers_count,
                dd.production_firms_count: self.production_firms_count,
                dd.production_firms_pct  : self.productions_firms_pct,
                }
        for k, v in col_val.items():
            od.loc[self.index_lbl, k] = v
        return od

    def ret_tickers_list(self):
        odf = pd.DataFrame()
        odf[self.index_lbl] = self.df[fc.Ticker].unique()
        return odf

def main():
    pass
    ##
    ws = rcf.load_whole_sample()
    ##
    _ws = ws[ws[fc.JMonth].ge(rm.pa.start_jmonth)]
    if rm.pa.end_jmonth is not None:
        _ws = _ws[_ws[fc.JMonth].le(rm.pa.end_jmonth)]

    bs = rcf.make_balanced_subsample(_ws,
                                     col2balance_across = fc.JMonth,
                                     target_column = fc.Ticker)
    ws_lbl = ds.whole_sample
    bs_lbl = ds.balanced_subsample
    ##
    df_dsc = pd.DataFrame()

    dsc_index = (ws_lbl, bs_lbl)
    data_dct = {ws_lbl: ws,
                bs_lbl: bs}

    for smpl in dsc_index:
        ddo = DataDsc(df = data_dct[smpl], the_index_lbl = smpl)
        od = ddo.ret_odf()
        df_dsc = df_dsc.append(od)

    df_dsc = df_dsc.convert_dtypes()
    cf.save_df_to_xl(df_dsc,
                     rdirs.data / f'{dfn.data_description}',
                     index = True,
                     float_format = "%.2f")

    init_month = df_dsc.at[bs_lbl, dd.initial_jmonth]
    last_month = df_dsc.at[bs_lbl, dd.final_jmonth]
    bs_pn = rdirs.data / f'{bs_lbl}-{init_month}-{last_month}.xlsx'
    cf.save_df_to_xl(bs,
                     bs_pn,
                     float_format = '%.3f')

    with open(rdirs.data / f'{dfn.bs_name_txt}.txt', 'w') as f:
        f.write(str(bs_pn))
    ##
    for smpl in dsc_index:
        ddo = DataDsc(df = data_dct[smpl], the_index_lbl = smpl)
        ou = ddo.ret_tickers_list()
        cf.save_df_to_xl(ou, rdirs.data / f'{smpl}-{dfn.firms}.xlsx')

##
if __name__ == '__main__':
    main()
else:
    pass
    ##
