##
import pandas as pd


try:
    from py import z_ns as ns
    from py import z_cf as cf
except ModuleNotFoundError:
    import z_ns as ns
    import z_cf as cf

lst_script = 'e'
script_name = 'f'

dirs = ns.ProjectDirectories()
rd = ns.RawDataColumns()
ft = ns.FirmTypes()

cur_prq = dirs.raw / f"{script_name}{ns.parquet_suf}"
pre_prq = dirs.raw / f"{lst_script}{ns.parquet_suf}"

def main():
    pass
    ##
    df = pd.read_parquet(pre_prq)
    df = df.sort_values([rd.PublishDateTime], ascending = False)
    df[rd.jDate] = df[rd.jDate].astype(int)
    df[rd.jMonth] = df[rd.jDate] // 100
    print(df)
    ##
    cd = df[rd.firmType].isin([ft.Service, ft.Production])
    cd &= df[rd.isBlank].ne('True')
    cd &= df[rd.succeed].eq('True')
    print(cd[cd])
    ##
    df = df[cd]
    print(df)
    ##
    df = df.drop_duplicates(subset = [rd.Symbol, rd.jMonth])
    print(df)
    ##
    df = df[
        [rd.TracingNo, rd.firmType, rd.Symbol, rd.jMonth, rd.PublishDateTime,
         rd.revUntilLastMonth, rd.modification, rd.revUntilLastMonthModified,
         rd.saleQ, rd.revenue, rd.revUntilCurrnetMonth]]
    ##
    for col in [rd.revUntilLastMonth, rd.modification,
                rd.revUntilLastMonthModified, rd.revenue,
                rd.revUntilCurrnetMonth, rd.saleQ]:
        df[col] = df[col].apply(lambda x: str(x).split('.')[0])
        df[col] = df[col].apply(lambda x: None if x == 'nan' else x)
    ##
    df[rd.modificationCheck] = False
    for el in [0, 1, -1]:
        df[rd.modificationCheck] |= df[
                                        rd.revUntilLastMonth].fillna(0).astype(
                int) + df[rd.modification].fillna(0).astype(int) == df[
                                        rd.revUntilLastMonthModified].fillna(0).astype(
                int) + el

    ch1 = df[rd.modificationCheck].eq(False)
    ch1df = df[ch1]
    print(ch1df)
    ##
    df.loc[ch1, rd.modification] = df[
                                       rd.revUntilLastMonthModified].fillna(0).astype(
            int) - df[rd.revUntilLastMonth].fillna(0).astype(int)
    print(df)
    ##
    for el in [0, 1, -1]:
        df[rd.modificationCheck] |= df[
                                        rd.revUntilLastMonth].fillna(0).astype(
                int) + df[rd.modification].fillna(0).astype(int) == df[
                                        rd.revUntilLastMonthModified].fillna(0).astype(
                int) + el
    ch1 = df[rd.modificationCheck].eq(False)
    ch1df = df[ch1]
    print(ch1df)
    ##
    ch2 = df[rd.revenue].isna()
    print(ch2[ch2])
    ##
    ch3 = df[rd.revenue].eq('0')
    ch3df = df[ch3]
    print(ch3df)
    ##
    ch4 = df[rd.saleQ].ne('0')
    ch4 &= df[rd.saleQ].notna()
    ch4df = df[ch4]
    print(ch4df)
    ##
    ch5 = ch3 & ch4
    ch5df = df[ch5]
    print(ch5df)
    ##
    df = df[~ ch5]
    print(df)
    ##
    ch6 = df[rd.revenue].eq('0')
    ch6 &= df[rd.saleQ].ne('0')
    ch6 &= df[rd.saleQ].notna()
    ch6 &= df[rd.firmType].ne(ft.Service)
    ch6df = df[ch6]
    print(ch6df)
    ##
    ch61 = ch3 & ~ ch5
    ch61df = df[ch61]
    print(ch61df)
    ##
    df[rd.untilCurMonthCheck] = False
    for el in [0, 1, -1]:
        df[rd.untilCurMonthCheck] |= df[
                                         rd.revUntilLastMonthModified].fillna(0).astype(
                int) + \
                                     df[rd.revenue].fillna(0).astype(int) == \
                                     df[
                                         rd.revUntilCurrnetMonth].fillna(0).astype(
                                             int) + el

    ch7 = df[rd.untilCurMonthCheck].eq(False)
    ch7df = df[ch7]
    print(ch7df)
    ##
    ch7 &= df[rd.revUntilLastMonthModified].notna()
    ch7 &= df[rd.revUntilLastMonthModified].ne('0')
    ch7df = df[ch7]
    print(ch7df)
    ##
    ch8 = df[rd.revenue].astype(int).lt(0)
    ch8df = df[ch8]
    print(ch8df)
    ##
    df4 = df[[rd.Symbol, rd.jMonth, rd.modification]]
    print(df4)
    ##
    df4[rd.jMonth] = df4[rd.jMonth].apply(lambda x: cf.find_n_month_before(x))
    ##
    df4[rd.modificationFromNextMonth] = df4[rd.modification]
    ##
    df4 = df4[[rd.Symbol, rd.jMonth, rd.modificationFromNextMonth]]
    ##
    df = df.merge(df4, how = 'left')
    ##
    df[rd.modifiedMonthRevenue] = df[rd.revenue].astype(int) + df[
        rd.modificationFromNextMonth].fillna(0).astype(int)
    ##
    df = df.applymap(str)
    df.to_parquet(cur_prq, index = False)
    print(df)

##
if __name__ == "__main__":
    main()
    print(f"{script_name}.py done!")
else:
    pass
    ##
