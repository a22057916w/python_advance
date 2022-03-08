import os, sys
import pandas as pd

import collections
import collections.abc
# the above packages are required for importing pptx, on Python 3.10.X+

from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

sys.path.append("./script")
from PPTX_FEATURE import Report, Font
from EXCEL_FEATURE import Workbook

import openpyxl


g_strOutputPath = os.path.join("./result", os.path.basename(__file__)[:-3] + ".pptx")



if __name__ == "__main__":
    Carnoustie = Workbook(openpyxl.load_workbook("/data/Code/python/python_advance/pptx/example/Carnoustie_Regulatory Schedule (HrP2 AX201)_20211217.xlsx"))
    # wb = openpyxl.load_workbook("/data/Code/python/python_advance/pptx/example/Carnoustie_Regulatory Schedule (HrP2 AX201)_20211217.xlsx")
    #
    # ws = wb.worksheets[1]
    # for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=4, max_col=6):
    #     for cell in row:
    #         if cell.column != 4:
    #             print(cell.column, end=" ")
    #     print()
