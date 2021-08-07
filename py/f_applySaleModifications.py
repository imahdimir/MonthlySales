##
import pandas as pd
import z_namespaces as ns
import z_classesFunctions as cf

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
    df[rd.jMonth] = df[rd.jDate].astype(int) // 100
    print(df)
    ##
    cnd = df[rd.firmType].isin([ft.Service, ft.Production])
    cnd &= df[rd.isBlank].ne('True')
    cnd &= df[rd.succeed].eq('True')
    print(cnd[cnd])
    ##
    df1 = df[cnd]
    print(df1)
    ##
    cnd1 = ~ df1.duplicated(subset = [rd.Symbol, rd.jMonth])
    df2 = df1[cnd1]
    print(df2)
    ##
    df2 = df2[
        [rd.TracingNo, rd.firmType, rd.Symbol, rd.jMonth, rd.PublishDateTime,
         rd.revUntilLastMonth, rd.modification, rd.revUntilLastMonthModified,
         rd.saleQ, rd.revenue, rd.revUntilCurrnetMonth]]
    ##
    for col in [rd.revUntilLastMonth, rd.modification,
                rd.revUntilLastMonthModified, rd.revenue,
                rd.revUntilCurrnetMonth, rd.saleQ]:
        df2[col] = df2[col].apply(lambda x: str(x).split('.')[0])
        df2[col] = df2[col].apply(lambda x: None if x == 'nan' else x)
    ##
    df2['ModificationCh'] = df2[rd.revUntilLastMonth].fillna(0).astype(int) + \
                            df2[rd.modification].fillna(0).astype(int) == df2[
                                rd.revUntilLastMonthModified].fillna(0).astype(
            int)
    df2['ModificationCh'] |= df2[rd.revUntilLastMonth].fillna(0).astype(int) + \
                             df2[rd.modification].fillna(0).astype(int) == df2[
                                 rd.revUntilLastMonthModified].fillna(0).astype(
            int) + 1
    df2['ModificationCh'] |= df2[rd.revUntilLastMonth].fillna(0).astype(int) + \
                             df2[rd.modification].fillna(0).astype(int) == df2[
                                 rd.revUntilLastMonthModified].fillna(0).astype(
            int) - 1
    ch1 = df2['ModificationCh'].eq(False)
    ch1df = df2[ch1]
    print(ch1df)
    ##
    df2.loc[ch1, rd.modification] = df2[
                                        rd.revUntilLastMonthModified].fillna(0).astype(
            int) - df2[rd.revUntilLastMonth].fillna(0).astype(int)
    print(df2)
    ##
    df2['ModificationCh'] = df2[rd.revUntilLastMonth].fillna(0).astype(int) + \
                            df2[rd.modification].fillna(0).astype(int) == df2[
                                rd.revUntilLastMonthModified].fillna(0).astype(
            int)
    df2['ModificationCh'] |= df2[rd.revUntilLastMonth].fillna(0).astype(int) + \
                             df2[rd.modification].fillna(0).astype(int) == df2[
                                 rd.revUntilLastMonthModified].fillna(0).astype(
            int) + 1
    df2['ModificationCh'] |= df2[rd.revUntilLastMonth].fillna(0).astype(int) + \
                             df2[rd.modification].fillna(0).astype(int) == df2[
                                 rd.revUntilLastMonthModified].fillna(0).astype(
            int) - 1
    ch1 = df2['ModificationCh'].eq(False)
    ch1df = df2[ch1]
    print(ch1df)
    ##
    ch2 = df2[rd.revenue].isna()
    print(ch2[ch2])
    ##
    ch3 = df2[rd.revenue].eq('0')
    ch3df = df2[ch3]
    print(ch3df)
    ##
    ch4 = df2[rd.saleQ].ne('0')
    ch4 &= df2[rd.saleQ].notna()
    ch4df = df2[ch4]
    print(ch4df)
    ##
    ch5 = ch3 & ch4
    ch5df = df2[ch5]
    print(ch5df)
    ##
    df3 = df2[~ ch5]
    print(df3)
    ##
    ch6 = df3[rd.revenue].eq('0')
    ch6 &= df3[rd.saleQ].ne('0')
    ch6 &= df2[rd.saleQ].notna()
    ch6 &= df3[rd.firmType].ne(ft.Service)
    ch6df = df3[ch6]
    print(ch6df)
    ##
    ch61 = ch3 & ~ ch5
    ch61df = df3[ch61]
    print(ch61df)
    ##
    df3['UntilCurMCh'] = df3[
                             rd.revUntilLastMonthModified].fillna(0).astype(int) + \
                         df3[rd.revenue].fillna(0).astype(int) == df3[
                             rd.revUntilCurrnetMonth].fillna(0).astype(int)
    df3['UntilCurMCh'] |= df3[
                              rd.revUntilLastMonthModified].fillna(0).astype(int) + \
                          df3[rd.revenue].fillna(0).astype(int) == df3[
                              rd.revUntilCurrnetMonth].fillna(0).astype(int) + 1
    df3['UntilCurMCh'] |= df3[
                              rd.revUntilLastMonthModified].fillna(0).astype(int) + \
                          df3[rd.revenue].fillna(0).astype(int) == df3[
                              rd.revUntilCurrnetMonth].fillna(0).astype(int) - 1
    ch7 = df3['UntilCurMCh'].eq(False)
    ch7df = df3[ch7]
    print(ch7df)
    ##
    ch7 &= df3[rd.revUntilLastMonthModified].notna()
    ch7 &= df3[rd.revUntilLastMonthModified].ne('0')
    ch7df = df3[ch7]
    print(ch7df)
    ##
    ch8 = df3[rd.revenue].astype(int).lt(0)
    ch8df = df3[ch8]
    print(ch8df)
    ##
    df4 = df3[[rd.Symbol, rd.jMonth, rd.modification]]
    print(df4)
    ##
    df4[rd.jMonth] = df4[rd.jMonth].apply(lambda x: cf.find_n_month_before(x))
    ##
    df4['ModificationFromNextMonth'] = df4[rd.modification]
    ##
    df4 = df4[[rd.Symbol, rd.jMonth, 'ModificationFromNextMonth']]
    ##
    df3 = df3.merge(df4, how = 'left')
    ##
    df3['ModifiedMonthlyRev'] = df3[rd.revenue].astype(int) + df3[
        'ModificationFromNextMonth'].fillna(0).astype(int)
    ##
    df3 = df3.applymap(str)
    df3.to_parquet(cur_prq, index = False)
    print(df3)

##
if __name__ == "__main__":
    main()
    print(f"{script_name}.py done!")
