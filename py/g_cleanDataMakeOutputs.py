##
import pandas as pd
from scipy import stats
import numpy as np
from persiantools.jdatetime import JalaliDate
from py import z_namespaces as ns
import warnings

warnings.filterwarnings("ignore")

lst_script_name = 'f'
script_name = 'g'

dirs = ns.ProjectDirectories()
rd = ns.RawDataColumns()
ft = ns.FirmTypes()

cur_prq = dirs.raw / f"{script_name}{ns.parquet_suf}"
pre_prq = dirs.raw / f"{lst_script_name}{ns.parquet_suf}"

def main():
    pass
    ##
    df = pd.read_parquet(pre_prq)
    print(df)
    ##
    for col in [rd.revUntilLastMonth, rd.modification,
                rd.revUntilLastMonthModified, rd.revenue,
                rd.revUntilCurrnetMonth, rd.modifiedMonthRevenue]:
        df = df.rename(columns = {col: col + '_MR'})
    ##
    jtoday = JalaliDate.today()
    jyearnow = str(jtoday.year)
    jmonthnow = str(jtoday.month)
    jdaynow = str(jtoday.day) if jtoday.day > 9 else f'0{jtoday.day}'
    full_data_n = 'MonthlySale-FullData-' + jyearnow + jmonthnow + jdaynow

    print(full_data_n)

    df.to_excel(dirs.outputs / f"{full_data_n}.xlsx", index = False)
    df.to_parquet(dirs.outputs / f"{full_data_n}{ns.parquet_suf}",
                  index = False)
    ##
    month_sale = df[[rd.firmType, rd.Symbol, rd.jMonth, rd.PublishDateTime,
                     rd.modifiedMonthRevenue + '_MR']]
    print(month_sale)
    ##
    month_sale[rd.modifiedMonthRevenue + '_BT'] = month_sale[
                                                      rd.modifiedMonthRevenue + '_MR'].astype(
            int) / (10 * 10 ** 3)
    ##
    month_sale = month_sale.drop(columns = rd.modifiedMonthRevenue + '_MR')
    ##
    month_sale.loc[month_sale[rd.modifiedMonthRevenue + '_BT'].between(-0.001,
                                                                       0.001), rd.modifiedMonthRevenue + '_BT'] = 0
    ##
    month_sale = month_sale[month_sale[rd.modifiedMonthRevenue + '_BT'].ne(0)]
    print(month_sale)
    ##
    month_sale2 = month_sale[
        month_sale[rd.firmType].isin([ft.Production, ft.Service])]
    print(month_sale2)
    ##
    z_scores = stats.zscore(month_sale2[rd.modifiedMonthRevenue + '_BT'])
    abs_z_scores = np.abs(z_scores)
    filter_outliers = abs_z_scores < 3
    month_sale2 = month_sale2[filter_outliers]
    print(month_sale2)
    ##
    df2 = month_sale2[month_sale2[rd.modifiedMonthRevenue + '_BT'].lt(0)]
    print(df2)
    ##
    month_sale2 = month_sale2[
        [rd.firmType, rd.Symbol, rd.jMonth, rd.modifiedMonthRevenue + '_BT']]
    ##
    month_sale2.to_parquet(cur_prq, index = False)
    ##
    final_data_n = 'MonthlySale-' + jyearnow + jmonthnow + jdaynow
    print(final_data_n)
    ##
    # for col in month_sale2.columns:
    #     month_sale2[col] = month_sale2[col].astype(str)
    ##
    month_sale2 = month_sale2.convert_dtypes()
    ##
    month_sale2.to_excel(dirs.outputs / f"{final_data_n}.xlsx", index = False)

    month_sale2.to_parquet(dirs.outputs / f"{final_data_n}{ns.parquet_suf}",
                           index = False)

##
if __name__ == '__main__':
    main()
    print(f"{script_name}.py done!")
else:
    pass
    ##
