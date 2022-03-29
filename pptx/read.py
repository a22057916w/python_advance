import collections
import collections.abc
# the above packages are required for importing pptx, on Python 3.10.X+

from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

def read_pptx(strPPTXFilePath):
    clientRT = Presentation(strPPTXFilePath)

    slides = clientRT.slides

    sld = slides[0]
    for shape in sld.shapes:
        if shape.has_table:
            print("------------------------")
            table = shape.table
            #table_to_df(table, row_idx_count=3)
            for row in range(len(table.rows)):
                for col in range(len(table.columns)):
                    print("(%d, %d) %s" % (row, col, table.cell(row, col).text_frame.text), end=" ")
                print()
            return

read_pptx("/data/Code/python/python_advance/pptx/result/report.pptx")
