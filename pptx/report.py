import os
import pandas as pd


import collections
import collections.abc
# the above packages are required for importing pptx, on Python 3.10.X+

from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

class cFont():
    def __init__(self, *, name = "Calibri", size = Pt(12), color = RGBColor(0,0,255), bold = True, italic = True):
        self.name = name
        self.size = size
        self.color = color
        self.bold = bold
        self.italic = italic


class PptxReport():

    table = [[None]*0]

    def __init__(self):
        self.prs = Presentation()
        print(self.prs.slide_height)

    def save(self, strOutputPath):
        self.prs.save(strOutputPath)

    def add_slide(self, layout_idx):
        slide_layout = self.prs.slide_layouts[layout_idx]
        self.prs.slides.add_slide(slide_layout)

    def get_slide(self, slide_idx):
        return self.prs.slides[slide_idx]

    def add_table_from_dataFrame(self, df, slide_idx, left = 0, top = 0):
        shapes = self.prs.slides[slide_idx].shapes
        #print(len(shapes))
        left = Inches(left)
        top = Inches(top)
        width = height = Inches(0)

        rows = df.shape[0] + 1
        cols = df.shape[1]

        table = shapes.add_table(rows, cols, left, top, width, height).table
        # print(type(shapes.parent))
        # print(len(shapes))
        # print("********************")
        for col in range(df.shape[1]):
            table.columns[col].height = Inches(2.0)
            for row in range(df.shape[0] + 1):
                if row == 0:
                    table.cell(row, col).text = str(df.columns[col])
                    continue
                table.cell(row, col).text = str(df.iloc[row - 1, col])
                # type(table.cell(row, col).text_frame.paragraphs) return 'tuple'

        self.table[slide_idx].append(table)     # save table to a list of slides

        return table

    # format the column bwidth and text size
    def resize_table(self, table, font_size):
        # setting font size
        for col in range(len(table.columns)):
            for row in range(len(table.rows)):
                for cell_pt in table.cell(row, col).text_frame.paragraphs:
                    cell_pt.font.size = Font_size
        # format the column by finding the max length paragraphs
        list_col_max_width = [0 for x in range(len(table.columns))]
        for col in range(len(table.columns)):
            for row in range(len(table.rows)):
                for cell_pt in table.cell(row, col).text_frame.paragraphs:
                    list_col_max_width[col] = max(list_col_max_width[col], len(cell_pt.text)*(font_size))
        # setting column width
        for col in range(len(table.columns)):
            table.columns[col].width = list_col_max_width[col] + Cm(0.25)


    # fill cell background
    def fill_cell(self, table, list_cells, RGBcolor):
        for row, col in list_cells:
            cell = table.cell(row, col)
            fill = cell.fill
            fill.solid()
            fill.fore_color.rgb = RGBcolor

    # font cell text
    def font_cell(self, table, list_cells, cFont):
        for row, col in list_cells:
            cell = table.cell(row, col)
            for paragraph in cell.text_frame.paragraphs:
                for run in paragraph.runs:
                    font = run.font
                    self.setFont(font, cFont)

    # concatenate text to a cell
    def add_text_to_cell(self, strText, table, row, col, cFont):
        cell = table.cell(row, col)
        paragraph = cell.text_frame.paragraphs[-1]
        run = paragraph.add_run()
        run.text = strText
        font = run.font
        self.setFont(font, cFont)


    def setFont(self, font, myFont):
        font.name = myFont.name
        font.size = myFont.size
        font.color.rgb = myFont.color
        font.bold = myFont.bold
        font.italic = myFont.italic

    def setAlign(self, cell, align_type):
        for paragraph in cell.text_frame.paragraphs:
            paragraph.alignment = align_type

if __name__ == "__main__":
    strOutputPath = os.path.join("./result", os.path.basename(__file__)[:-3] + ".pptx")
    df = pd.read_excel("./data/test.xlsx")


    pptxRT = PptxReport()
    pptxRT.add_slide(0)
    slide = pptxRT.get_slide(0)

    table = pptxRT.add_table_from_dataFrame(df, 0, 0, 0)

    resize_font_size = Pt(12)
    pptxRT.resize_table(table, resize_font_size)
    myFont = cFont(size=Pt(10), color=RGBColor(0,0,255))

    pptxRT.fill_cell(table, [(1,1),(2,3)], RGBColor(255,0,0))
    pptxRT.font_cell(table, [(2,2),(3,3)], myFont)
    pptxRT.add_text_to_cell("asdfasdf", table, 3, 5, myFont)

    pptxRT.resize_table(table, resize_font_size)
    pptxRT.save(strOutputPath)

    # prs = Presentation()
    # title_only_slide_layout = prs.slide_layouts[5]
    # print(df)
    # print(df.iloc[1, 1])
    # df.iloc[1, 1] = "sdfsdfsfdsdfsdfsdf\nsfsdfsdfsdfsd"
    # print(len(df.iloc[:, 0]))
    # print(df.shape[0] + 1)
    # print(df.columns[0])

    df2 = pd.read_excel("./data/test2.xlsx")

    slide = pptxRT.get_slide(0)
    table2 = pptxRT.add_table_from_dataFrame(df2, 0, 0, 0)

    resize_font_size = Pt(12)
    pptxRT.resize_table(table2, resize_font_size = Pt(12))

    myFont = cFont(size=Pt(12), color=RGBColor(0,0,255))
    pptxRT.fill_cell(table2, [(1,1),(2,3)], RGBColor(255,0,0))
    pptxRT.font_cell(table2, [(2,2),(3,3)], myFont)
    pptxRT.add_text_to_cell("asdfasdf", table2, 3, 5, resize_font_size)

    pptxRT.resize_table(table2, myFont)
    pptxRT.save(strOutputPath)


    # print(df)
    # print("*"*20)
    # print(df.shape)
    # print(df.shape[1])
