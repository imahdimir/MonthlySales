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
