import os
import pandas as pd


import collections
import collections.abc
# the above packages are required for importing pptx, on Python 3.10.X+

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor


class PptxReport():

    def __init__(self):
        self.prs = Presentation()

    def save(self, strOutputPath):
        self.prs.save(strOutputPath)

    def add_slide(self, layout_idx):
        slide_layout = self.prs.slide_layouts[layout_idx]
        self.prs.slides.add_slide(slide_layout)

    def get_slide(self, slide_idx):
        return self.prs.slides[slide_idx]

    def add_table_from_dataFrame(self, slide, df):
        shapes = slide.shapes

        left = top = Inches(0)
        width = height = Inches(0)

        rows = df.shape[0] + 1
        cols = df.shape[1]

        table = shapes.add_table(rows, cols, left, top, width, height).table
        # print("SDFFDSFDFSDFSDFSDFSDFSDFD")
        # print(type(shapes))
        # print(type(table))
        for col in range(df.shape[1]):
            table.columns[col].height = Inches(2.0)
            for row in range(df.shape[0] + 1):
                if row == 0:
                    table.cell(row, col).text = str(df.columns[col])
                    continue
                table.cell(row, col).text = str(df.iloc[row - 1, col])
                # type(table.cell(row, col).text_frame.paragraphs) return 'tuple'
        return table

    # format the column bwidth and text size
    def format_table(self, table, font_size):
        # setting font size
        for col in range(len(table.columns)):
            for row in range(len(table.rows)):
                for cell_pt in table.cell(row, col).text_frame.paragraphs:
                    cell_pt.font.size = Pt(font_size)

        # format the column by finding the max length paragraphs
        list_col_max_width = [0 for x in range(len(table.columns))]
        for col in range(len(table.columns)):
            for row in range(len(table.rows)):
                for cell_pt in table.cell(row, col).text_frame.paragraphs:
                    list_col_max_width[col] = max(list_col_max_width[col], len(cell_pt.text)*Pt(font_size))

        # setting column width
        for col in range(len(table.columns)):
            table.columns[col].width = list_col_max_width[col]

    def color_cell(self, table, list_cells, RGBcolor):
        for row, col in list_cells:
            cell = table.cell(row, col)
            fill = cell.fill
            fill.solid()
            fill.fore_color.rgb = RGBcolor


if __name__ == "__main__":
    strOutputPath = os.path.join("./result", os.path.basename(__file__)[:-3] + ".pptx")
    df = pd.read_excel("./data/test.xlsx")


    pptxRT = PptxReport()
    pptxRT.add_slide(0)
    slide = pptxRT.get_slide(0)
    table = pptxRT.add_table_from_dataFrame(slide, df)
    pptxRT.format_table(table, 12)
    pptxRT.color_cell(table, [(1,1),(2,3)], RGBColor(255,0,0))
    pptxRT.save(strOutputPath)

    # prs = Presentation()
    # title_only_slide_layout = prs.slide_layouts[5]
    print(df)
    print(df.iloc[1, 1])
    df.iloc[1, 1] = "sdfsdfsfdsdfsdfsdf\nsfsdfsdfsdfsd"
    print(len(df.iloc[:, 0]))
    print(df.shape[0] + 1)
    print(df.columns[0])


    # print(df)
    # print("*"*20)
    # print(df.shape)
    # print(df.shape[1])
