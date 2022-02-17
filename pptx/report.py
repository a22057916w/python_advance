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

# if __name__ == "__main__":
    # strOutputPath = os.path.join("./result", os.path.basename(__file__)[:-3] + ".pptx")
    # df = pd.read_excel("./data/test.xlsx")
    #
    #
    # pptxRT = PptxReport()
    # pptxRT.add_slide(0)
    # pptxRT.add_picture(0, "./data/dontlaught.jpg")
    # slide = pptxRT.get_slide(0)
    #
    # table = pptxRT.add_table_from_dataFrame(df, 0, 0, 0)
    #
    # resize_font_size = Pt(12)
    # pptxRT.resize_table(table, resize_font_size)
    # myFont = cFont(size=Pt(10), color=RGBColor(0,0,255))
    #
    # pptxRT.fill_cell(table, [(1,1),(2,3)], RGBColor(255,0,0))
    # pptxRT.font_cell(table, [(2,2),(3,3)], myFont)
    # pptxRT.add_text_to_cell("asdfasdf", table, 3, 5, myFont)
    #
    # pptxRT.resize_table(table, resize_font_size)
    # pptxRT.save(strOutputPath)
    #
    # # prs = Presentation()
    # # title_only_slide_layout = prs.slide_layouts[5]
    # # print(df)
    # # print(df.iloc[1, 1])
    # # df.iloc[1, 1] = "sdfsdfsfdsdfsdfsdf\nsfsdfsdfsdfsd"
    # # print(len(df.iloc[:, 0]))
    # # print(df.shape[0] + 1)
    # # print(df.columns[0])
    #
    # df2 = pd.read_excel("./data/test2.xlsx")
    #
    # slide = pptxRT.get_slide(0)
    # table2 = pptxRT.add_table_from_dataFrame(df2, 0, 0, 0)
    #
    # resize_font_size = Pt(12)
    # pptxRT.resize_table(table2, resize_font_size)
    #
    # myFont = cFont(size=Pt(12), color=RGBColor(0,0,255))
    # pptxRT.fill_cell(table2, [(1,1),(2,3)], RGBColor(255,0,0))
    # pptxRT.font_cell(table2, [(2,2),(3,3)], myFont)
    # pptxRT.add_text_to_cell("asdfasdf", table2, 3, 5, myFont)
    #
    # pptxRT.resize_table(table2, resize_font_size)
    # pptxRT.save(strOutputPath)


    # print(df)
    # print("*"*20)
    # print(df.shape)
    # print(df.shape[1])
