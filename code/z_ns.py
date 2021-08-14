##
from pathlib import Path
from varname import nameof as no


CWD = Path.cwd()


class Params:
    def __init__(self,
                 initial_jmonth_4balanced_subsample=139601,
                 last_jmonth=None):
        self.initial_jmonth = initial_jmonth_4balanced_subsample
        self.last_jmonth = last_jmonth


class Constants:
    def __init__(self):
        self.code_dirname = "Code"
        self.fdist_n = "TSE Monthly Sale Data Project"
        self.firms = None
        self.base_year = None
        self.empty_xl_col = ""

        for key, att in self.__dict__.items():
            if att is None:
                self.__dict__[key] = key


class Dirs:
    def __init__(self):
        """ds."""
        cte = Constants()
        # in main dir
        self.Code = cte.code_dirname
        self.fdist = None  # formal distribution of the project
        self.in_cpi_dollar_1xl = None
        self.figs = None
        self.out_data = None

        for key, val in self.__dict__.items():
            if val is None:
                self.__dict__[key] = CWD / key
            else:
                self.__dict__[key] = CWD / val

                # in /Code/
        self.jsons = None
        self.htmls = None
        self.raw = None
        self.texdata = None

        for att_k in [no(self.jsons), no(self.htmls), no(self.raw)]:
            self.__dict__[att_k] = self.Code / att_k

        # /fdist/
        self.FormalDist = self.fdist / cte.fdist_n
        self.data = None
        self.data = self.FormalDist / no(self.data)

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
        self.data_desc = None

        self.vars = None

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


class DataSetsNames:
    def __init__(self):
        self.whole_sample = None
        self.balanced_subsample = None

        for attr_key in self.__dict__:
            self.__dict__[attr_key] = attr_key


class DataDescriptionCols:
    def __init__(self):
        self.initial_jmonth = None
        self.final_jmonth = None
        self.obs = None
        self.month_count = None
        self.firms_count = None
        self.production_firms_count = None
        self.production_firms_pct = None
        self.avg_obs_monthly = None

        for attr_key in self.__dict__:
            self.__dict__[attr_key] = attr_key


class MonthlyStatCols:
    def __init__(self):
        self.rev_Hemmat = "Revenue(Hemat)"
        self.mean_rev_ht = "Mean Revenue(Hemat)"
        self.normed_cpi = "Normalized CPI"
        self.rev_r = "Real Revenue(Hemat)"
        self.rev_d = "Revenue(B$)"
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
