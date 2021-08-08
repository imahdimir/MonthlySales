##
from pathlib import Path


CWD = Path.cwd()

# % Constants %%%%%%%%%%%%%%%%%%%%%%%%%%%%
parquet_suf = ".parquet"
html_suf = '.html'
ul = '_'  # under line

class ProjectDirectories:
    def __init__(self):
        self.htmls = None
        self.jsons = None
        self.outputs = None
        self.raw = None

        for attr_key in self.__dict__:
            self.__dict__[attr_key] = CWD / attr_key

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

class RawSaleDataKeys:
    def __init__(self):
        self.Symbol = None
        self.JDate = None
        self.Title = None
        self.FullHtmlUrl = None

        keys_helper = []
        for attr_key in self.__dict__:
            self.__dict__[attr_key] = attr_key
            keys_helper.append(attr_key)

        self.keys = keys_helper

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
