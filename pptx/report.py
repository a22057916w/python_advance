import os, sys
import pandas as pd
import numpy as np

import collections
import collections.abc
# the above packages are required for importing pptx, on Python 3.10.X+

from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

sys.path.append("./script")
from PPTX_FEATURE import Report, Font

g_strOutputPath = os.path.join("./result", os.path.basename(__file__)[:-3] + ".pptx")

def create_pptx():
    pptxRT = Report()

    df = pd.read_excel("./data/test.xlsx")

    pptxRT.add_slide(0)
    pptxRT.add_picture(0, "./data/dontlaught.jpg")
    slide = pptxRT.get_single_slide(0)

    table = pptxRT.add_table_from_dataFrame(df, 0, 0, 0)

    resize_font_size = Pt(12)
    pptxRT.resize_table(table, resize_font_size)
    myFont = Font(size=Pt(10), color=RGBColor(0,0,255))

    pptxRT.fill_cell(table, [(1,1),(2,3)], RGBColor(255,0,0))
    pptxRT.font_cell(table, [(2,2),(3,3)], myFont)
    pptxRT.add_text_to_cell("asdfasdf", table, 3, 5, myFont)

    pptxRT.resize_table(table, resize_font_size)
    pptxRT.save(g_strOutputPath)

    df2 = pd.read_excel("./data/test2.xlsx")

    slide = pptxRT.get_single_slide(0)
    table2 = pptxRT.add_table_from_dataFrame(df2, 0, 0, 0)

    resize_font_size = Pt(12)
    pptxRT.resize_table(table2, resize_font_size)

    myFont = Font(size=Pt(12), color=RGBColor(0,0,255))
    pptxRT.fill_cell(table2, [(1,1),(2,3)], RGBColor(255,0,0))
    pptxRT.font_cell(table2, [(2,2),(3,3)], myFont)
    pptxRT.add_text_to_cell("asdfasdf", table2, 3, 5, myFont)

    pptxRT.resize_table(table2, resize_font_size)
    pptxRT.save(g_strOutputPath)


def read_pptx(strPPTXFilePath):
    clientRT = Report(strPPTXFilePath)
    slides = clientRT.get_slides()
    clientRT.save("./result/report_read.pptx")
    sld = slides[3]
    for shape in sld.shapes:
        if shape.has_table:
            print("------------------------")
            table = shape.table
            df = clientRT.read_table_as_dataFrame(table, row_header_count=3)
            print(df)
            # for row in range(len(table.rows)):
            #     for col in range(len(table.columns)):
            #         print("(%d, %d) %s" % (row, col, table.cell(row, col).text_frame.text), end=" ")
            #     print()
            return

def table_to_df(table, *, row_idx_count="1"):

    row_headers = []
    for i in range(row_idx_count):
        column_name = []
        for col in range(len(table.columns)):
            column_name.append(table.cell(i, col).text_frame.text)
        row_headers.append(column_name)

    print(row_headers)

    row_data = []
    for row in range(row_idx_count, len(table.rows)):
        col_data = []
        for col in range(len(table.columns)):
            col_data.append(table.cell(row, col).text_frame.text)
        row_data.append(col_data)

    print(row_data)

    row_mutil_index = pd.MultiIndex.from_arrays(row_headers)
    df = pd.DataFrame(row_data, columns=row_mutil_index)

    print(df)
    #return df

if __name__ == "__main__":
    #create_pptx()
    read_pptx("./example/Carnoustie_Mid Deep Dive_Regulatory schedule_20210225.pptx")
    # print(df)
    # print("*"*20)
    # print(df.shape)
    # print(df.shape[1])
