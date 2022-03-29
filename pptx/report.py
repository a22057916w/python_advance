import os, sys
import pandas as pd
from datetime import datetime
import time
import logging
import traceback


import collections
import collections.abc
# the above packages are required for importing pptx, on Python 3.10.X+

from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR



sys.path.append("./script")
from PPTX_FEATURE import PresentationFeature as PF
from EXCEL_FEATURE import DataFrameFeature as DFF
from EXCEL_FEATURE import WorkBookFeature as WBF
import openpyxl

# [Main]
g_strVersion = "1.0.0.1"

# [Client Excel]
g_strExcelPath = "./example/Carnoustie_Regulatory Schedule (HrP2 AX201)_20211217.xlsx"

# [PPT Output]
g_strOutputPath = os.path.join("./result", os.path.basename(__file__)[:-3] + ".pptx")


class CLIENTREPORT():
    def __init__(self, pptx_path):
        self.prs = Presentation(pptx_path)

    def get_table_dict(self, slide_idx):
        try:
            slide = self.prs.slides[slide_idx]

            list_table = []
            for shape in sld.shapes:
                if shape.has_table:
                    list_table.append(shape.table)

            # for slide 1 only
            list_status_table_title = ["RFD, RTS, RTO", "LABEL", "DVT 1.0 ETA", "DVT 2.0 ETA"]
            dict_table = {}
            for table in list_table:
                title = self.get_table_title(table, 1, 0)
                if title in list_status_table_title:
                    dict_table["Status"] = table
                elif title == "System":
                    dict_table["System"] = table
                else:
                    dict_table["Module"] = table
            return dict_table
        except:
            self.module_logger.error("Unexpected Error : " + str(traceback.format_exc()))
            return None

    def get_table_title(self, table, row, col):
        try:
            cell = table.cell(row, col)
            if cell.value == None:
                self.moduel_logger.error("The given cell value is empty.")
                return None
            else:
                return cell.value
        except:
            self.module_logger.error("Unexpected Error : " + str(traceback.format_exc()))
            return None


class PPTXREPORT():
    # store data of sheet "Post-RTS" from excel
    df_postRTS_MD = None
    df_postRTS_VOL = None

    prs = Presentation()

    def __init__(self):
        try:
            self.strLogPath = os.path.join(os.getcwd(), os.path.basename(__file__)[:-3] + ".log")
            self.module_logger = setup_logger("module_logger", self.strLogPath)

            self.module_logger.info("========= Initiating =========")

            self.module_logger.info("Reading and Setting Workbook")
            WBF.set_workbook("./example/Carnoustie_Regulatory Schedule (HrP2 AX201)_20211217.xlsx")

            # start the construction flow
            self.startFlow()

        except Exception as e:
            self.module_logger.error("Unexpected Error: " + str(e))
            sys.exit(1)

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

                self.prs.save(g_strOutputPath)

            self.module_logger.info("========== End ==========")
        except Exception as e:
            self.module_logger.info("Unexpected Error: " + str(e))

    # read the excel sheet "Post-RTS"
    def read_postRTS(self, excel_path):
        try:
            # read the excel sheet "Post-RTS" and skip first row
            df_raw = pd.read_excel(excel_path, sheet_name="Post-RTS", skiprows=1)

            # parse "P-RTS country (Mandatory):" table as df
            self.df_postRTS_MD = DFF.truncate(df_raw, column=0, first_value="P-RTS country (Mandatory):", last_value="P-RTS Country (Voluntary):")          # get the part by spilt the raw df
            self.df_postRTS_MD = DFF.drop_na_row(self.df_postRTS_MD)    # get rid of rows with all NaN value in every column
            DFF.filter_column_value(self.df_postRTS_MD, column_name="Country", sep="(")

            # parse "P-RTS country (Voluntary)):" table as df
            self.df_postRTS_VOL = DFF.truncate(df_raw, column=0, first_value="P-RTS Country (Voluntary):", last_value=DFF.NaN)
            self.df_postRTS_VOL = DFF.drop_na_row(self.df_postRTS_VOL)
            self.df_postRTS_VOL = DFF.drop_row(self.df_postRTS_VOL, 0)  # drop first row since it is dupicated to columns

            return True
        except Exception as e:
            self.module_logger.info("Unexpected Error: " + str(e))
            return False

    # Construct the slide "Carnoustie Regulatory status summary"
    def add_regulatory_status_summary_slide(self):
        try:
            slide_layout = self.prs.slide_layouts[0]    # zero for blank slide
            self.prs.slides.add_slide(slide_layout)

            b_flowResult = True

            if b_flowResult:
                self.module_logger.info("Writing Title")
                b_flowResult = self.write_regulatory_status_summary_title(5, 0, Pt(12)*37, Pt(12))
            if b_flowResult:
                self.module_logger.info("Creating System Level Table")
                b_flowResult = self.create_system_level_table(0.20, 0.63, 2, 2)
            if b_flowResult:
                self.module_logger.info("Creating Module Level Table")
                b_flowResult = self.create_module_level_table(0.20, 4.30, 3, 2)
            if b_flowResult:
                self.module_logger.info("Creating Status-Date Table")
                b_flowResult = self.create_status_date_table(7.88, 0.05)
            if b_flowResult:
                self.prs.save(g_strOutputPath)
                return True
            else:
                return False
        except Exception as e:
            self.module_logger.info("Unexpected Error: " + str(e))
            return False

    # write the slide title "Carnoustie Regulatory status summary", whick Carnoustie is project name
    def write_regulatory_status_summary_title(self, left, top, width, height, slide_idx=0):
        try:
            slide = self.prs.slides[slide_idx]

            project_name = WBF.get_cell_value(sheetname="S&G&E Schedu_DVT2 Start", pos="B1")
            text = project_name + " Regulatory status summary"

            txbox = PF.add_textbox(slide, text, left, top, width, height)

            # set textbox style
            txbox.left = txbox.left - int(txbox.width / 2)
            PF.set_textbox_alignment(txbox, PP_ALIGN.CENTER)

            return True
        except Exception as e:
            self.module_logger.info("Unexpected Error: " + str(e))
            return False

    # construct the system level table in slide "Carnoustie Regulatory status summary"
    def create_system_level_table(self, left, top, row, col, slide_idx=0):
        try:
            slide = self.prs.slides[slide_idx]
            shapes = slide.shapes

            table = PF.add_table(slide, row, col, left, top)

            # construct cell(1,0) and (0,1) which are row title and column name
            table.cell(1,0).text = "System"
            table.cell(0,1).text = "PPE"

            # construct cell(1, 1) which contain county info
            total_ctry, list_ctry = DFF.get_country_set(self.df_postRTS_MD, category="Host")
            table.cell(1,1).text = "%d\n" % total_ctry          # set total country number(no duplicated)
            PF.add_text_with_newlines(table.cell(1,1), list_ctry, string_len=20)

            # set table style
            PF.set_table_text_size(table, size=Pt(8))
            PF.set_column_width(table, [0, 1], [Pt(11)*6, Pt(6)*40])
            PF.set_table_alignment(table, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
            PF.set_table_fill(table, RGBColor(255, 255, 255))   # !!! the border must be set before the fill, or the xml would be overide
            PF.set_cell_fill(table, [(0, 0), (0, 1)], RGBColor(0, 133, 195))
            PF.set_table_border(table)

            return True
        except Exception as e:
            self.module_logger.info("Unexpected Error :" + str(e))
            return False

    # construct the module level table in slide "Carnoustie Regulatory status summary"
    def create_module_level_table(self, left, top, row, col, slide_idx=0):
        try:
            slide = self.prs.slides[slide_idx]
            shapes = slide.shapes

            table = PF.add_table(slide, row, col, left, top)

            # set column 1 title name
            table.cell(0,1).text = "PPE"

            # construct the column 0 (row title) by rows
            list_title = [WBF.get_WWAN_ID()+"\n(WWAN)", "RFID"]
            for i in range(1, row):
                table.cell(i, 0).text = list_title[i - 1]

            # construct the column 1 (country info) by rows
            list_ctgy = ["Host_WWAN", "RFID"]
            for i in range(1, row):
                total_ctry, list_ctry = DFF.get_country_set(self.df_postRTS_MD, category=list_ctgy[i - 1])
                table.cell(i, 1).text = "%d\n" % total_ctry          # set total country number(no duplicated)
                PF.add_text_with_newlines(table.cell(i, 1), list_ctry, string_len=20)

            # set table style
            PF.set_table_text_size(table, size=Pt(8))
            PF.set_column_width(table, [0, 1], [Pt(11)*6, Pt(6)*40])
            PF.set_table_alignment(table, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
            PF.set_table_border(table)    # !!! the border must be set before the fill, or the xml would be overide
            PF.set_table_fill(table, RGBColor(255, 255, 255))
            PF.set_cell_fill(table, [(0, 0), (0, 1)], RGBColor(0, 133, 195))

            return True
        except Exception as e:
            self.module_logger.info("Unexpected Error :" + str(e))
            return False

    # construct the status table which located on the right-top side of slied
    def create_status_date_table(self, left, top, slide_idx=0):
        try:
            list_status = ["RFD", "RTS", "RTO"]
            list_date = []

            list_target_cell = ["F7", "F8", "F9"]
            for cell_pos in list_target_cell:
                date_value = WBF.get_cell_value(sheetname="S&G&E Schedu_DVT2 Start", pos=cell_pos)  # return <datetime>
                list_date.append(datetime.strftime(date_value, "%Y/%m/%d"))

            df_status = pd.DataFrame(data={"Ststus": list_status, "Date": list_date})

            slide = self.prs.slides[slide_idx]
            shapes = slide.shapes

            # new table by df
            table = PF.add_table_by_df(slide, df_status, left, top)

            # set table style
            PF.resize_table(table, Pt(10))
            PF.set_table_fill(table, RGBColor(255, 240, 201))
            PF.set_table_text_color(table, RGBColor(0, 0, 0))
            PF.set_table_border(table, str(RGBColor(255, 240, 201)))

            return True
        except Exception as e:
            self.module_logger.info("Unexpected Error :" + str(e))
            return False

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
    #Carnoustie = PPTXREPORT()
    ClientRT = CLIENTREPORT("/data/Code/python/python_advance/pptx/result/report.pptx")
