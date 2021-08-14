""""""

##
import pandas as pd

from Code import z_ns as ns
from Code import z_cf as cf
from Code import a_main as ma


dirs = ns.Dirs()
fc = ns.FormalCols()
ds = ns.DataSetsNames()
dd = ns.DataDescriptionCols()
ft = ns.FirmTypes()
vif = ns.VeryImportantFiles()
cte = ns.Constants()

pa = ma.pa


class DataDsc:
    def __init__(self, df: pd.DataFrame, the_index_lbl: str):
        self.df = df
        self.index_lbl = the_index_lbl
        self.odf = pd.DataFrame(index=[the_index_lbl])


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


def make_the_balanced_subsample_save():
    whs = cf.load_whole_sample()
    whs = whs[whs[fc.JMonth].ge(pa.initial_jmoneh)]
    if pa.last_jmonth is not None:
        whs = whs[whs[fc.JMonth].le(pa.last_jmonth)]
    bsu = cf.make_balanced_subsample(whs, fc.JMonth, fc.Ticker)
    init_jm = pa.initial_jmoneh
    lst_jm = whs[fc.JMonth].max()
    bs_lbl = ds.balanced_subsample
    bsu_pn = dirs.out_data / f'{bs_lbl}-{init_jm}-{lst_jm}.xlsx'
    cf.save_df_to_xl(bsu,
                     bsu_pn,
                     float_format='%.3f')
    with open(dirs.raw / f'{vif.bs_name}.txt', 'w') as f:
        f.write(str(bsu_pn))
        print(bsu_pn)
    return bsu


def main():
    pass
    ##
    ws = cf.load_whole_sample()
    bs = make_the_balanced_subsample_save()
    ws_lbl = ds.whole_sample
    bs_lbl = ds.balanced_subsample

    df_dsc = pd.DataFrame()
    dsc_index = (ws_lbl, bs_lbl)
    data_dct = {ws_lbl: ws,
                bs_lbl: bs}
    for smpl in dsc_index:
        ddo = DataDsc(df=data_dct[smpl], the_index_lbl=smpl)
        od = ddo.ret_odf()
        df_dsc = df_dsc.append(od)
    df_dsc = df_dsc.convert_dtypes()
    cf.save_df_to_xl(df_dsc,
                     dirs.out_data / f'{vif.data_desc}',
                     index=True,
                     float_format="%.3f")
    ##
    for smpl in dsc_index:
        ddo = DataDsc(df=data_dct[smpl], the_index_lbl=smpl)
        ou = ddo.ret_tickers_list()
        cf.save_df_to_xl(ou, dirs.out_data / f'{smpl}-{cte.firms}.xlsx')
    ##


##
if __name__ == '__main__':
    main()
else:
    pass
    ##
