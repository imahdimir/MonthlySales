##
from py import z_ns as ns
from varname import nameof


r_py = ns.ReportMaker / 'py'

class FormalReportDirectories:
    def __init__(self):
        super().__init__()

        self.dirname = "TSE Monthly Sale Data Project"
        self.dirpath = ns.ReportMaker / self.dirname

        self.code = None
        self.data = None
        self.figs = None

        for attr_key in self.__dict__:
            if self.__dict__[attr_key] is None:
                self.__dict__[attr_key] = self.dirpath / attr_key

        self.raw = None
        self.raw = self.code / nameof(self.raw)

class Parameters:
    def __init__(self):
        self.start_jmonth = None
        self.end_jmonth = None

class DataFilesNames(FormalReportDirectories):
    def __init__(self):
        super().__init__()

        self.data_description = None
        self.firms = None
        self.bs_name_txt = None

        for attr_key in self.__dict__:
            self.__dict__[attr_key] = attr_key

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
