import os, sys
import pandas as pd

import collections
import collections.abc
# the above packages are required for importing pptx, on Python 3.10.X+

from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

import logging

sys.path.append("./script")
from PPTX_FEATURE import PresentationFeature as PF
from EXCEL_FEATURE import DataFrameFeature as DFF

import openpyxl

# [Main]
g_strVersion = "1.0.0.1"

# [Client Excel]
g_strExcelPath = "/data/Code/python/python_advance/pptx/example/Carnoustie_Regulatory Schedule (HrP2 AX201)_20211217.xlsx"

# [PPT Output]
g_strOutputPath = os.path.join("./result", os.path.basename(__file__)[:-3] + ".pptx")


class PPTXREPORT():
    # store data of sheet "Post-RTS" from excel
    df_postRTS_MD = None
    df_postRTS_VOL = None

    prs = Presentation()

    def __init__(self):
        self.strLogPath = os.path.join(os.getcwd(), os.path.basename(__file__)[:-3] + ".log")
        self.module_logger = setup_logger("module_logger", self.strLogPath)

        #self.module_logger.info("========= Initiating =========")

        self.startFlow()

    def startFlow(self):
        self.module_logger.info("========== Start ==========")
        self.module_logger.info("Python " + sys.version)
        self.module_logger.info("%s.py %s" % (os.path.basename(__file__)[:-3], g_strVersion))
        #self.module_logger.info("Decteing User: %s\n" % self.strUser)

        try:
            b_flowResult = True

            if b_flowResult:
                self.module_logger.info("Read the excel sheet \"Post-RTS\"")
                b_flowResult = self.read_postRTS(g_strExcelPath)
            if b_flowResult:
                self.module_logger.info("Construct the slide \"Carnoustie Regulatory status summary\"")
                b_flowResult = self.add_regulatory_status_summary_slide()

        except Exception as e:
            self.module_logger.info("Unexpected Error: " + str(e))

    def read_postRTS(self, excel_path):
        try:
            # read the excel sheet "Post-RTS" and skip first row
            df_raw = pd.read_excel(excel_path, sheet_name="Post-RTS", skiprows=1)

            # parse "P-RTS country (Mandatory):" table as df
            self.df_postRTS_MD = DFF.truncate(df_raw, column=0, first_value="P-RTS country (Mandatory):", last_value="P-RTS Country (Voluntary):")          # get the part by spilt the raw df
            self.df_postRTS_MD = DFF.drop_na_row(self.df_postRTS_MD)    # get rid of rows with all NaN value in every column
            DFF.filter_column_value(self.df_postRTS_MD, column_name="Country", sep="(")
            # for val in self.df_postRTS_MD["Country"]:
            #     print(val, type(val))
            print(self.df_postRTS_MD["Country"])
            # parse "P-RTS country (Voluntary)):" table as df
            self.df_postRTS_VOL = DFF.truncate(df_raw, column=0, first_value="P-RTS Country (Voluntary):", last_value=DFF.NaN)
            self.df_postRTS_VOL = DFF.drop_na_row(self.df_postRTS_VOL)
            self.df_postRTS_VOL = DFF.drop_row(self.df_postRTS_VOL, 0)  # drop first row since it is dupicated to columns

            return True
        except Exception as e:
            self.module_logger.info("Unexpected Error: " + str(e))
            return False

    def add_regulatory_status_summary_slide(self):
        slide_layout = self.prs.slide_layouts[0]    # zero for blank slide
        self.prs.slides.add_slide(slide_layout)

        self.create_level_table(self.df_postRTS_MD, table_name="System", column_name="PPE", slide_idx=0)

        self.prs.save(g_strOutputPath)

    # need migrate
    def create_level_table(self, df, *, table_name, column_name, slide_idx):
        shapes = self.prs.slides[slide_idx].shapes

        left = Inches(0)
        top = Inches(0)
        width = height = Inches(1)

        rows = 2
        cols = 2

        table = shapes.add_table(rows, cols, left, top, width, height).table
        table.cell(1,0).text = table_name
        table.cell(0,1).text = column_name


        PF.resize_table(table, Pt(10))

def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)-5s][%(lineno)-3d][%(funcName)s] %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
    fh.setFormatter(formatter)

    # define a Handler which writes INFO messages or higher to the sys.stderr
    ch = logging.StreamHandler(sys.stdout)
    # ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # set a format which is simpler for console use
    formatter = logging.Formatter('%(levelname)-5s - %(lineno)-4d - %(funcName)s : %(message)s')
    # tell the handler to use this format
    ch.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


if __name__ == "__main__":
    Carnoustie = PPTXREPORT()

    # wb = openpyxl.load_workbook("/data/Code/python/python_advance/pptx/example/Carnoustie_Regulatory Schedule (HrP2 AX201)_20211217.xlsx")
    #
    # ws = wb.worksheets[1]
    # for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=4, max_col=6):
    #     for cell in row:
    #         if cell.column != 4:
    #             print(cell.column, end=" ")
    #     print()
