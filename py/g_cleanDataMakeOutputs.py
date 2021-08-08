##
import pandas as pd
from scipy import stats
import numpy as np
from persiantools.jdatetime import JalaliDate
import warnings


try:
    from py import z_ns as ns
    from py import z_cf as cf
except ModuleNotFoundError:
    import z_ns as ns
    import z_cf as cf

warnings.filterwarnings("ignore")

lst_script_name = 'f'
script_name = 'g'

dirs = ns.ProjectDirectories()
rd = ns.RawDataColumns()
oc = ns.OutputColumns()
ft = ns.FirmTypes()
fc = ns.FormalCols()

cur_prq = dirs.raw / f"{script_name}{ns.parquet_suf}"
pre_prq = dirs.raw / f"{lst_script_name}{ns.parquet_suf}"

def main():
    pass
    ##
    df = pd.read_parquet(pre_prq)
    print(df)
    ##
    ren = {rd.revUntilLastMonth        : oc.revUntilLastMonth_MR,
           rd.modification             : oc.modification_MR,
           rd.revUntilLastMonthModified: oc.revUntilLastMonthModified_MR,
           rd.revenue                  : oc.revenue_MR,
           rd.revUntilCurrnetMonth     : oc.revUntilCurrnetMonth_MR,
           rd.modifiedMonthRevenue     : oc.modifiedMonthRevenue_MR}

    df = df.rename(columns = ren)
    ##
    jtoday = JalaliDate.today()
    jyearnow = str(jtoday.year)
    jmonthnow = str(jtoday.month)
    jdaynow = str(jtoday.day) if jtoday.day > 9 else f'0{jtoday.day}'
    # full_data_n = 'MonthlySale-FullData-' + jyearnow + jmonthnow + jdaynow

    # print(full_data_n)
    #
    # # df.to_excel(dirs.output / f"{full_data_n}.xlsx", index = False)
    # df.to_parquet(dirs.output / f"{full_data_n}{ns.parquet_suf}",
    #               index = False)
    ##
    month_sale = df[[rd.firmType, rd.Symbol, rd.jMonth, rd.PublishDateTime,
                     oc.modifiedMonthRevenue_MR]]
    print(month_sale)
    ##
    month_sale[oc.modifiedMonthRevenue_BT] = month_sale[
                                                 oc.modifiedMonthRevenue_MR].astype(
            int) / (10 * 10 ** 3)
    ##
    month_sale = month_sale.drop(columns = oc.modifiedMonthRevenue_MR)
    ##
    month_sale.loc[month_sale[oc.modifiedMonthRevenue_BT].between(-0.001,
                                                                  0.001), oc.modifiedMonthRevenue_BT] = 0
    ##
    month_sale = month_sale[month_sale[oc.modifiedMonthRevenue_BT].ne(0)]
    print(month_sale)
    ##
    month_sale2 = month_sale[
        month_sale[rd.firmType].isin([ft.Production, ft.Service])]
    print(month_sale2)
    ##
    z_scores = stats.zscore(month_sale2[oc.modifiedMonthRevenue_BT])
    abs_z_scores = np.abs(z_scores)
    filter_outliers = abs_z_scores < 3
    month_sale2 = month_sale2[filter_outliers]
    print(month_sale2)
    ##
    df2 = month_sale2[month_sale2[oc.modifiedMonthRevenue_BT].lt(0)]
    print(df2)
    ##
    month_sale2 = month_sale2[
        [rd.firmType, rd.Symbol, rd.jMonth, oc.modifiedMonthRevenue_BT]]
    ##
    month_sale2.to_parquet(cur_prq, index = False)
    ##
    final_data_n = 'TSE Monthly Sale-Updated ' + jyearnow + jmonthnow + jdaynow
    print(final_data_n)
    ##
    month_sale2 = month_sale2.convert_dtypes()
    ##
    formal_cols = {oc.firmType               : fc.FirmType,
                   oc.Symbol                 : fc.Ticker,
                   oc.jMonth                 : fc.JMonth,
                   oc.modifiedMonthRevenue_BT: fc.RevenueBT}
    formal_data = month_sale2.rename(columns = formal_cols)
    ##
    cf.save_df_to_xl(formal_data,
                     dirs.output / final_data_n,
                     float_format = "%.3f")

##
if __name__ == '__main__':
    main()
    print(f"{script_name}.py done!")
else:
    pass
    ##
