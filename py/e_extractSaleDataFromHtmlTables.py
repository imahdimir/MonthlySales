"""doc."""

##
import pandas as pd
from lxml import etree
import numpy as np
from multiprocessing import cpu_count
from multiprocessing import Pool
# from multiprocess import Pool
import re
from io import StringIO


try:
    from py import z_ns as ns
    from py import z_cf as cf
except ModuleNotFoundError:
    import z_ns as ns
    import z_cf as cf

parser = etree.HTMLParser()

lst_script_name = 'd'
script_name = 'e'

dirs = ns.ProjectDirectories()
rd = ns.RawDataColumns()
ft = ns.FirmTypes()
em = ns.ErrorMessages()

cur_prq = dirs.raw / f"{script_name}{ns.parquet_suf}"
pre_prq = dirs.raw / f"{lst_script_name}{ns.parquet_suf}"

current_period = ['دوره یک ماهه منتهی به']
sale_mil_rial = ['مبلغ فروش']
sum_row = ['جمع', 'Total Amount']
modif_keys = ['اصلاحات']
type_prod = ['تولید و فروش', 'محصولات']
type_serv = ['خدمات و فروش']
type_realstate = ['Building']
type_leasing = ['هزینه تامین منابع مالی عملیات لیزینگ محقق شده']
since_start_financial_year = ['از ابتدای سال مالی']
since_modified = ['اصلاح شده']
sale_quant = ['تعداد فروش', 'مقدار/تعداد فروش']
since_start_finyear_serv = ['تا پايان دوره مالي منتهي به']

current_period_srch = [cf.wos(x) for x in current_period]
sale_mil_srch = [cf.wos(x) for x in sale_mil_rial]
sum_row_srch = [cf.wos(x) for x in sum_row]
modif_srch = [cf.wos(x) for x in modif_keys]
type_prod_srch = [cf.wos(x) for x in type_prod]
type_serv_srch = [cf.wos(x) for x in type_serv]
since_start_financial_year_srch = [cf.wos(x) for x in
                                   since_start_financial_year]
since_modified_srch = [cf.wos(x) for x in since_modified]
sale_quant_srch = [cf.wos(x) for x in sale_quant]
since_start_finyear_serv_srch = [cf.wos(x) for x in since_start_finyear_serv]

outputs = [rd.isBlank, rd.firmType, rd.errMsg, rd.revUntilLastMonth,
           rd.hasModification, rd.modification, rd.revUntilLastMonthModified,
           rd.saleQ, rd.revenue, rd.revUntilCurrnetMonth, rd.succeed]

outputs_dct = cf.make_output_dict(outputs)

class FirmsMonthlySale:

    def __init__(self, tracingno, jdate):

        self.htmlpn = dirs.htmls / f'{tracingno}{ns.html_suf}'

        with open(self.htmlpn, 'r') as f:
            self.raw_html = f.read()

        self.jdate = int(jdate)
        self.jmonth = jdate // 100

        self.fixed_html = cf.fix_html(self.raw_html)
        self.tree = etree.parse(StringIO(self.fixed_html), parser)

        self.table = pd.read_html(self.fixed_html)[0]
        self.fixed_table = fix_table(self.table)

        self.date_df = self.fixed_table.applymap(cf.find_jdate)
        self.jmonth_df = self.date_df.applymap(lambda x: x // 100)

        self.output = outputs_dct.copy()

        self.output[rd.isBlank] = self.fixed_table.empty
        self.output[rd.firmType] = self.find_firmtype()
        self.output[rd.hasModification] = True

        self.sum_row = None
        self.sale_cols = None
        self.cur_per_cells = None
        self.cur_per_cols = None
        self.modification_cols = None
        self.since_start_cols = None
        self.prev_month = cf.find_n_month_before(self.jmonth)
        self.prev_month_cols = None
        self.modified_cols = None
        self.cur_jdate_cols = None

    def find_firmtype(self):
        for elem in self.tree.xpath("//table[@id]"):
            for el in ft.firmTypesList:
                if el in elem.attrib["id"]:
                    return el
            if cf.any_of_list_isin(type_realstate, elem.attrib['id']):
                return ft.RealEstate
        for elem in self.tree.xpath("//div"):
            if elem.text:
                if cf.any_of_list_isin(type_prod_srch, cf.wos(elem.text)):
                    return ft.Production
                if cf.any_of_list_isin(type_serv_srch, cf.wos(elem.text)):
                    return ft.Service
                if cf.any_of_list_isin(type_leasing, elem.text):
                    return ft.Leasing
        return ft.unknown

    def find_current_period_cols(self):
        cur_per_ch = self.fixed_table.applymap(lambda x: cf.any_of_list_isin(
                current_period_srch,
                x))
        self.cur_per_cells = cf.find_all_locs_eq_val(cur_per_ch, True)
        self.cur_per_cols = [x[1] for x in self.cur_per_cells]

    def find_sum_row(self):
        sum_row_check = self.fixed_table.isin(sum_row_srch)
        sum_row_locs = cf.find_all_locs_eq_val(sum_row_check, True)
        if len(sum_row_locs) == 0:
            sum_row_locs = [(self.fixed_table.shape[0] - 1, 0)]
        self.sum_row = sum_row_locs[0][0]

    def find_sale_cols(self):
        sale_check = self.fixed_table.applymap(lambda x: cf.any_of_list_isin(
                sale_mil_srch,
                x))
        sale_locs = cf.find_all_locs_eq_val(sale_check, True)
        self.sale_cols = [x[1] for x in sale_locs]
        return self.sale_cols

    def find_current_jdate(self):
        cur_m = cf.find_all_locs_eq_val(self.date_df, self.jdate)
        self.cur_jdate_cols = [x[1] for x in cur_m]

    def check_current_period_jdate(self):
        yrm = self.date_df.applymap(lambda x: x // 100)
        jyrm = self.jdate // 100
        date_locs = cf.find_all_locs_eq_val(yrm, jyrm)
        date_month_intersect = list(set(self.cur_per_cells) & set(date_locs))
        if len(date_month_intersect) == 0:
            self.output[rd.errMsg] = em.dateConflict

    def find_modif_cols(self):
        modi_check = self.fixed_table.applymap(lambda x: str(x) in modif_srch)
        modi_locs = cf.find_all_locs_eq_val(modi_check, True)
        if len(modi_locs) == 0:
            self.output[rd.hasModification] = False
            return None
        self.modification_cols = [x[1] for x in modi_locs]

    def find_since_start_finyear_prod(self):
        since_start_ch = self.fixed_table.applymap(lambda x: cf.any_of_list_isin(
                since_start_financial_year_srch,
                str(x)))
        since_start_locs = cf.find_all_locs_eq_val(since_start_ch, True)
        if len(since_start_locs) > 0:
            self.since_start_cols = [x[1] for x in since_start_locs]

    def find_prev_m_cols(self):
        prev_m_ch = cf.find_all_locs_eq_val(self.jmonth_df, self.prev_month)
        if len(prev_m_ch) > 0:
            self.prev_month_cols = [x[1] for x in prev_m_ch]
        return self.prev_month_cols

    def find_rev_until_last_month_modified_prod(self):
        modified_ch = self.fixed_table.applymap(lambda x: cf.any_of_list_isin(
                since_modified_srch,
                x))
        modified_locs = cf.find_all_locs_eq_val(modified_ch, True)
        if len(modified_locs) == 0:
            return None
        self.modified_cols = [x[1] for x in modified_locs]
        if pd.isnull([self.modified_cols, self.since_start_cols,
                      self.prev_month_cols, self.sale_cols]).any():
            return None
        until_last_m_modified = list(set(self.modified_cols) & set(self.since_start_cols) & set(
                self.prev_month_cols) & set(self.sale_cols))
        if len(until_last_m_modified) == 1:
            until_last_m_modified = until_last_m_modified[0]
            self.output[
                rd.revUntilLastMonthModified] = cf.read_accvalue_from_str(str(
                    self.fixed_table.at[self.sum_row, until_last_m_modified]))

    def find_rev_until_last_month_not_modified_prod(self):
        if pd.isnull([self.since_start_cols, self.prev_month_cols,
                      self.sale_cols]).any():
            return None
        until_last_not_modified = list(set(self.since_start_cols) & set(self.prev_month_cols) & set(
                self.sale_cols))
        until_last_not_modified = list(set(until_last_not_modified) - set(self.modified_cols))
        if len(until_last_not_modified) == 1:
            until_last_not_modified = until_last_not_modified[0]
            self.output[rd.revUntilLastMonth] = cf.read_accvalue_from_str(str(
                    self.fixed_table.at[self.sum_row, until_last_not_modified]))

    def find_until_current_month(self):
        if pd.isnull([self.since_start_cols, self.cur_jdate_cols,
                      self.sale_cols]).any():
            return None
        until_cur_m = list(set(self.since_start_cols) & set(self.cur_jdate_cols) & set(
                self.sale_cols))
        if len(until_cur_m) == 1:
            until_cur_m = until_cur_m[0]
            self.output[
                rd.revUntilCurrnetMonth] = cf.read_accvalue_from_str(str(
                    self.fixed_table.at[self.sum_row, until_cur_m]))

    def find_sale_quant(self):
        sale_q_ch = self.fixed_table.applymap(lambda x: str(x) in sale_quant_srch)
        sale_q_locs = cf.find_all_locs_eq_val(sale_q_ch, True)
        sale_q_cols = [x[1] for x in sale_q_locs]
        sale_q_cur_per = list(set(self.cur_per_cols) & set(sale_q_cols))
        if len(sale_q_cur_per) != 1:
            self.output[rd.errMsg] = rd.saleQ
            return None
        sale_q_cur_per = sale_q_cur_per[0]
        sale_qs = self.fixed_table[sale_q_cur_per]
        self.output[rd.saleQ] = 0
        for el in sale_qs:
            if re.fullmatch(r'\d*', el):
                self.output[rd.saleQ] += float(el)
        return self.output[rd.saleQ]

    def cur_m_rev_prod(self):
        m_sale_col = list(set(self.cur_per_cols) & set(self.sale_cols))
        if len(m_sale_col) == 0:
            self.output[rd.errMsg] = em.noMonthSaleIntersect
            return None
        m_sale_col = m_sale_col[0]
        self.output[rd.revenue] = cf.read_accvalue_from_str(str(
                self.fixed_table.at[self.sum_row, m_sale_col]))

    def prod_modification(self):
        if not self.output[rd.hasModification]:
            return None
        modi_sale_intersec = list(set(self.modification_cols) & set(self.sale_cols))
        if len(modi_sale_intersec) == 0:
            self.output[rd.hasModification] = False
            self.output[rd.errMsg] = em.noModificationSaleIntersect
            return None
        elif len(modi_sale_intersec) == 1:
            modi_sale_intersec_col = modi_sale_intersec[0]
            self.output[rd.modification] = cf.read_accvalue_from_str(str(
                    self.fixed_table.at[self.sum_row, modi_sale_intersec_col]))

    def production(self):
        self.find_since_start_finyear_prod()
        self.find_prev_m_cols()
        self.find_rev_until_last_month_modified_prod()
        self.find_rev_until_last_month_not_modified_prod()
        self.find_until_current_month()
        self.find_sale_quant()
        if self.output[rd.errMsg] is not None:
            return None
        self.cur_m_rev_prod()
        if self.output[rd.errMsg] is not None:
            return None
        self.prod_modification()

    def serive_cur_rev(self):
        if len(self.cur_per_cols) != 1:
            self.output[rd.errMsg] = em.notCurrentPeriod
            return None
        cur_per = self.cur_per_cols[0]
        self.output[rd.revenue] = cf.read_accvalue_from_str(str(
                self.fixed_table.at[self.sum_row, cur_per]))

    def service_modi(self):
        if not self.output[rd.hasModification]:
            return None
        if len(self.modification_cols) == 1:
            self.modification_cols = self.modification_cols[0]
            self.output[rd.modification] = cf.read_accvalue_from_str(str(
                    self.fixed_table.at[self.sum_row, self.modification_cols]))

    def find_since_start_finyear_serv(self):
        since_start_ch = self.fixed_table.applymap(lambda x: cf.any_of_list_isin(
                since_start_finyear_serv_srch,
                x))
        since_start_locs = cf.find_all_locs_eq_val(since_start_ch, True)
        if len(since_start_locs) > 0:
            self.since_start_cols = [x[1] for x in since_start_locs]
        return self.since_start_cols

    def find_rev_until_last_m_modified_serv(self):
        modified_ch = self.fixed_table.applymap(lambda x: cf.any_of_list_isin(
                since_modified_srch,
                x))
        modified_locs = cf.find_all_locs_eq_val(modified_ch, True)
        if len(modified_locs) == 0:
            return None
        self.modified_cols = [x[1] for x in modified_locs]
        if pd.isnull([self.modified_cols, self.since_start_cols,
                      self.prev_month_cols]).any():
            return None
        until_last_m_modified = list(set(self.modified_cols) & set(self.since_start_cols) & set(
                self.prev_month_cols))
        if len(until_last_m_modified) == 1:
            until_last_m_modified = until_last_m_modified[0]
            self.output[
                rd.revUntilLastMonthModified] = cf.read_accvalue_from_str(str(
                    self.fixed_table.at[self.sum_row, until_last_m_modified]))

    def find_rev_until_last_m_not_modified_serv(self):
        if pd.isnull([self.since_start_cols, self.prev_month_cols]).any():
            return None
        until_last_not_modified = list(set(self.since_start_cols) & set(self.prev_month_cols))
        if pd.isnull([until_last_not_modified, self.modified_cols]).any():
            return None
        until_last_not_modified = list(set(until_last_not_modified) - set(self.modified_cols))
        if len(until_last_not_modified) == 1:
            until_last_not_modified = until_last_not_modified[0]
            self.output[rd.revUntilLastMonth] = cf.read_accvalue_from_str(str(
                    self.fixed_table.at[self.sum_row, until_last_not_modified]))

    def find_until_current_month_serv(self):
        if pd.isnull([self.since_start_cols, self.cur_jdate_cols]).any():
            return None
        until_cur_m = list(set(self.since_start_cols) & set(self.cur_jdate_cols))
        if len(until_cur_m) == 1:
            until_cur_m = until_cur_m[0]
            self.output[
                rd.revUntilCurrnetMonth] = cf.read_accvalue_from_str(str(
                    self.fixed_table.at[self.sum_row, until_cur_m]))

    def service(self):
        self.find_since_start_finyear_serv()
        self.find_prev_m_cols()
        self.find_rev_until_last_m_modified_serv()
        self.find_rev_until_last_m_not_modified_serv()
        self.find_until_current_month_serv()
        self.serive_cur_rev()
        self.service_modi()

    def process_and_make_output(self):
        if not self.output[rd.firmType] in [ft.Production, ft.Service]:
            return self.output

        self.find_current_period_cols()

        if self.output[rd.errMsg] is not None:
            return self.output

        self.find_sum_row()
        self.find_sale_cols()
        self.find_current_jdate()

        if self.output[rd.errMsg] is not None:
            return self.output

        self.check_current_period_jdate()

        if self.output[rd.errMsg] is not None:
            return self.output

        self.find_modif_cols()

        if self.output[rd.firmType] == ft.Production:
            self.production()

        elif self.output[rd.firmType] == ft.Service:
            self.service()

        self.output[rd.succeed] = False
        if re.fullmatch(r"-?\d+\.\d*", str(self.output[rd.revenue])):
            self.output[rd.succeed] = True

        return self.output

def fix_table(indf):
    indf = indf.dropna(how = "all")
    indf = indf.dropna(how = "all", axis = 1)
    indf = indf.T.reset_index().T.reset_index()
    indf = indf.applymap(cf.wos)
    indf = indf.applymap(lambda x: np.nan if len(x) >= 100 else x)
    indf = indf.reset_index(drop = True)
    return indf

def target(tracingno, jdate):
    out1 = outputs_dct.copy()
    try:
        rep_obj = FirmsMonthlySale(tracingno, jdate)
        output = rep_obj.process_and_make_output()
        # print(tracingno)
        # print(output.values())
        return list(output.values())
    except ValueError as e:
        # noinspection PyTypeChecker
        out1[rd.errMsg] = em.ValueError
        out1[rd.succeed] = False
        print(tracingno)
        print(e)
        return list(out1.values())

def main():
    pass
    ##
    df = pd.read_parquet(pre_prq)
    print(df)
    ##
    df[outputs] = None
    ##
    for col in df.columns:
        df[col] = df[col].astype(str)
    ##
    df = cf.update_with_last_data(df, cur_prq)
    print(df)
    ##
    df[rd.TracingNo] = df[rd.TracingNo].astype(int)
    df[rd.htmlDownloaded] = df[rd.TracingNo].apply(lambda x: (
            dirs.htmls / f"{x}{ns.html_suf}").exists())
    ##
    cond = df[rd.htmlDownloaded].eq(True)
    print(cond[cond])
    ##
    cond &= df[rd.succeed].ne('True')
    print(cond[cond])
    ##
    cond &= df[rd.isBlank].ne('True')
    print(cond[cond])
    ##
    flt = df[cond]
    print(flt)
    ##
    cores_n = cpu_count()
    print(f'Num of cores : {cores_n}')
    clusters = cf.return_clusters_indices(flt)
    pool = Pool(cores_n)
    ##
    for i in range(0, len(clusters) - 1):
        start_i = clusters[i]
        end_i = clusters[i + 1]
        print(f"{start_i} to {end_i}")

        corr_is = flt.iloc[start_i:end_i].index

        tracnos = df.loc[corr_is, rd.TracingNo].astype(str)
        jdates = df.loc[corr_is, rd.jDate].astype(int)

        out = pool.starmap(target, zip(tracnos, jdates))

        for j, out_el in enumerate(outputs):
            df.loc[corr_is, out_el] = [w[j] for w in out]
        # break
    ##
    for col in df.columns:
        df[col] = df[col].astype(str)
    ##
    df.to_parquet(cur_prq, index = False)
    print(df)
    ##
    cond2 = df[rd.htmlDownloaded].eq('True')
    cond2 &= df[rd.succeed].eq('False')
    # cond2 &= ~ df['FirmType'].isin([m.firmtypes['b'], m.firmtypes['i'],
    #                                 m.firmtypes['r'], m.firmtypes['l']])
    cond2 &= df[rd.isBlank].ne('True')
    print(cond2[cond2])
    ##
    flt2 = df[cond2]
    ##
    print('Unsucceeded:')
    print(flt2)
    ##
    cond3 = df[rd.htmlDownloaded].eq('True')
    cond3 &= df[rd.succeed].ne('True')
    cond3 &= df[rd.isBlank].ne('True')
    cond3 &= ~ df[rd.firmType].isin([ft.Bank, ft.Insurance, ft.RealEstate,
                                     ft.Leasing])
    print(cond3[cond3])
    ##
    df3 = df[cond3]
    print(df3)
    ##
    manualy_checked = [750527, 240154, 245682, 630521, 233485]
    df.loc[
        df[rd.TracingNo].astype(int).isin(manualy_checked) & df[rd.errMsg].ne(
                'nan'), rd.isBlank] = 'True'
    ##
    df.to_parquet(cur_prq, index = False)
    print(df)

##
if __name__ == '__main__':
    main()
    print(f'{script_name}.py Done!')
else:
    pass
    ##
