""""""

##
import pandas as pd
from Code import ns as ns
from Code import cf as cf
import main as ma


idx = pd.Index

dirs = ns.Dirs()
fc = ns.FormalCols()
ft = ns.FirmTypes()
vif = ns.VeryImportantFiles()
cte = ns.Constants()
td = ns.TexDataFilenames()
stc = ns.SumStatCols()

pa = ma.pa

class DataDsc:
    def __init__(self, df: pd.DataFrame, the_index_lbl: str):
        self.df = df
        self.indexLbl = the_index_lbl
        self.odf = pd.DataFrame(index=[the_index_lbl])

        self.obs = df.shape[0]
        self.monthsNo = df[fc.JMonth].unique().size
        self.avgObsMonthly = self.obs / self.monthsNo
        self.initJMonth = df[fc.JMonth].min()
        self.lastJMonth = df[fc.JMonth].max()
        self.firmsNo = df[fc.Ticker].unique().size
        self.productionNo = df[df[fc.FirmType].eq(ft.Production)][
            fc.Ticker].unique().size
        self.productionPct = self.productionNo / self.firmsNo

    def ret_odf(self):
        od = self.odf
        col_val = {
                stc.obs          : self.obs,
                stc.initJMonth   : self.initJMonth,
                stc.lastJMonth   : self.lastJMonth,
                stc.monthsNo     : self.monthsNo,
                stc.avgObsMonthly: self.avgObsMonthly,
                stc.firmsNo      : self.firmsNo,
                stc.productionNo : self.productionNo,
                stc.productionPct: self.productionPct,
                }
        for k, v in col_val.items():
            od.loc[self.indexLbl, k] = v
        return od

    def ret_tickers_list(self):
        odf = pd.DataFrame()
        odf[self.indexLbl] = self.df[fc.Ticker].unique()
        return odf

def make_the_balanced_subsample_save():
    whs = cf.load_whole_sample()
    whs = whs[whs[fc.JMonth].ge(pa.initJMonth)]
    if pa.lastJMonth is not None:
        whs = whs[whs[fc.JMonth].le(pa.lastJMonth)]
    bsu = cf.make_balanced_subsample(whs, fc.JMonth, fc.Ticker)
    init_jm = pa.initJMonth
    lst_jm = whs[fc.JMonth].max()
    bs_lbl = cte.Balanced
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

    data = {cte.Whole   : ws,
            cte.Balanced: bs}
    ##
    df_dsc = pd.DataFrame()
    for k, v in data.items():
        ddo = DataDsc(df=v, the_index_lbl=k)
        od = ddo.ret_odf()
        df_dsc = df_dsc.append(od)
    df_dsc = df_dsc.convert_dtypes()
    cf.save_df_to_xl(df_dsc,
                     dirs.out_data / f'{vif.DatasetsSummaryStats}',
                     index=True,
                     float_format="%.3f")
    cf.add_to_texdata(td.sumStat, df_dsc)
    ##
    for k, v in data.items():
        ddo = DataDsc(df=v, the_index_lbl=k)
        ou = ddo.ret_tickers_list()
        cf.save_df_to_xl(ou, dirs.out_data / f'{k}-{cte.firms}.xlsx')

##
if __name__ == '__main__':
    main()
else:
    pass
    ##

    ##
