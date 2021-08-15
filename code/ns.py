##
from pathlib import Path
from varname import nameof as no


CWD = Path.cwd()

class BalancedSubsampleConfig:
    def __init__(self,
                 initial_jmonth_4balanced_subsample=139601,
                 last_jmonth=None):
        self.initJMonth = initial_jmonth_4balanced_subsample
        self.lastJMonth = last_jmonth

class Constants:
    def __init__(self):
        self.fdist_n_man = "TSE Monthly Sale Data Project"
        self.Whole = None
        self.Balanced = None
        self.firms = None
        for key, att in self.__dict__.items():
            if att is None:
                self.__dict__[key] = key

class Dirs:
    def __init__(self):
        """ds."""

        cte = Constants()

        # /main dir/
        self.Code = None
        self.docs = None
        self.data = None
        for key, val in self.__dict__.items():
            if val is None:
                self.__dict__[key] = CWD / key
            else:
                self.__dict__[key] = CWD / val

        # /code/
        self.raw = None
        self.raw = self.Code / 'UpdateData/raw'
        self.Analysis = None
        self.UpdateData = None
        for di in [no(self.Analysis), no(self.UpdateData)]:
            self.__dict__[di] = self.Code / di

        # /data/
        self.fdist = None  # formal distribution of the project
        self.in_cpi_dollar_1xl = None
        self.figs = None
        self.out_data = None
        self.jsons = None
        self.htmls = None
        l1 = [no(self.fdist),  # formal distribution of the project
              no(self.in_cpi_dollar_1xl),
              no(self.figs),
              no(self.out_data),
              no(self.jsons),
              no(self.htmls),
              ]
        for di in l1:
            self.__dict__[di] = self.data / di

        # /fdist/
        self.FormalDist = self.fdist / cte.fdist_n_man
        self.Fdata = self.FormalDist / 'data'
        self.FCode = self.FormalDist / 'code'
        self.Ffigs = self.FormalDist / 'figs'

        # /docs/
        self.texdata = None
        self.texdata = self.docs / no(self.texdata)

    def mkdir(self):
        for attr_key in self.__dict__:
            if not self.__dict__[attr_key].exists():
                self.__dict__[attr_key].mkdir()

class VeryImportantFiles:
    def __init__(self):
        dirs = Dirs()

        self.pgs = None
        self.pgs = dirs.raw / f"{no(self.pgs)}.txt"

        self.lastData = None
        self.lastData = dirs.raw / f'{no(self.lastData)}.txt'

        self.bs_name = None
        self.DatasetsSummaryStats = None

        for key, att in self.__dict__.items():
            if att is None:
                self.__dict__[key] = key

class TexDataFilenames:
    def __init__(self):
        self.vars = None  # single variables in text
        self.sumStat = None

        for key, att in self.__dict__.items():
            if att is None:
                self.__dict__[key] = key

class SumStatCols:
    def __init__(self):
        self.obs = None
        self.initJMonth = None
        self.lastJMonth = None
        self.monthsNo = None
        self.avgObsMonthly = None
        self.firmsNo = None
        self.productionNo = None
        self.productionPct = None

        for key, att in self.__dict__.items():
            if att is None:
                self.__dict__[key] = key

class DollarCpiCols:
    def __init__(self):
        # jmonth from formal cols
        self.Dollar = None
        self.CPI = None
        #

        for key, att in self.__dict__.items():
            if att is None:
                self.__dict__[key] = key

class ReqParams:
    def __init__(self):
        self.search_url = "https://search.codal.ir/api/search/v2/q"
        self.params = {
                "LetterType"       : "58",
                "AuditorRef"       : "-1",
                "Category"         : "3",
                "Childs"           : "false",
                "CompanyState"     : "-1",
                "CompanyType"      : "1",
                "Consolidatable"   : "true",
                "IsNotAudited"     : "false",
                "Length"           : "-1",
                "Mains"            : "true",
                "NotAudited"       : "true",
                "Audited"          : "true",
                "NotConsolidatable": "true",
                "PageNumber"       : "1",
                "Publisher"        : "false",
                "TracingNo"        : "-1",
                "search"           : "false", }
        self.CodalBaseUrl = "https://codal.ir"
        self.LetterCodeForMonthlySaleReorts = "ن-۳۰"

class CodalTableColumns:
    def __init__(self):
        self.TracingNo = None
        self.SuperVision = None
        self.Symbol = None
        self.CompanyName = None
        self.UnderSupervision = None
        self.Title = None
        self.LetterCode = None
        self.SentDateTime = None
        self.PublishDateTime = None
        self.HasHtml = None
        self.Url = None
        self.HasExcel = None
        self.HasPdf = None
        self.HasXbrl = None
        self.HasAttachment = None
        self.AttachmentUrl = None
        self.PdfUrl = None
        self.ExcelUrl = None
        self.XbrlUrl = None
        self.TedanUrl = None

        # codal_table_cols = ['TracingNo', 'SuperVision', 'Symbol', 'CompanyName','UnderSupervision', 'Title', 'LetterCode','SentDateTime', 'PublishDateTime', 'HasHtml', 'Url','HasExcel', 'HasPdf', 'HasXbrl', 'HasAttachment','AttachmentUrl', 'PdfUrl', 'ExcelUrl', 'XbrlUrl','TedanUrl']
        colslist = []
        for attr_key in self.__dict__:
            self.__dict__[attr_key] = attr_key
            colslist.append(attr_key)

        self.cols_list = colslist

class RawDataColumns(CodalTableColumns):
    def __init__(self):
        super().__init__()

        self.jDate = None
        self.fullUrl = None
        self.htmlDownloaded = None
        self.isBlank = None
        self.firmType = None
        self.errMsg = None
        self.revUntilLastMonth = None
        self.hasModification = None
        self.modification = None
        self.revUntilLastMonthModified = None
        self.saleQ = None
        self.revenue = None
        self.revUntilCurrnetMonth = None
        self.succeed = None
        self.jMonth = None
        self.modificationCheck = None
        self.untilCurMonthCheck = None
        self.modificationFromNextMonth = None
        self.modifiedMonthRevenue = None

        for attr_key in self.__dict__:
            self.__dict__[attr_key] = attr_key

class FirmTypes:
    def __init__(self):
        self.Production = None
        self.Service = None
        self.Insurance = None
        self.Leasing = None
        self.Bank = None
        self.RealEstate = None

        firmtypes_helper = []
        for attr_key in self.__dict__:
            self.__dict__[attr_key] = attr_key
            firmtypes_helper.append(attr_key)

        self.firmTypesList = firmtypes_helper
        self.unknown = 'unknown'

class ErrorMessages:
    def __init__(self):
        self.dateConflict = None
        self.noMonthSaleIntersect = None
        self.noModificationSaleIntersect = None
        self.notCurrentPeriod = None
        self.ValueError = None

        for attr_key in self.__dict__:
            self.__dict__[attr_key] = attr_key

class OutputColumns(RawDataColumns):
    def __init__(self):
        super().__init__()

        self.revUntilLastMonth_MR = None
        self.modification_MR = None
        self.revUntilLastMonthModified_MR = None
        self.revenue_MR = None
        self.revUntilCurrnetMonth_MR = None
        self.modifiedMonthRevenue_MR = None
        self.modifiedMonthRevenue_BT = None

        for attr_key in self.__dict__:
            self.__dict__[attr_key] = attr_key

class FormalCols(OutputColumns):
    def __init__(self):
        super().__init__()

        self.FirmType = 'FirmType'
        self.JMonth = 'JMonth'
        self.Ticker = 'Ticker'
        self.RevenueBT = 'Revenue(BT)'

class MonthlyStatCols:
    def __init__(self):
        self.rev_Hemmat = "Revenue(Hemat)"
        self.mean_rev_ht = "Mean Revenue(Hemat)"
        self.normed_cpi = "Normalized CPI"
        self.rev_r = "Real Revenue(Hemat)"
        self.rev_d = "Revenue(B Dollar)"
        self.norm_rev = "Normalized Revenue"
        self.norm_rev_r = "Normalized Real Revenue"
        self.norm_rev_d = "Normalized Dollar Revenue"

##
if __name__ == '__main__':
    pass
else:
    pass
    ##

##
