import os, sys
import pandas as pd


import collections
import collections.abc
# the above packages are required for importing pptx, on Python 3.10.X+

from pptx import Presentation
from pptx.util import Inches, Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE, MSO_ANCHOR
from pptx.oxml.xmlchemy import OxmlElement


class Font():
    def __init__(self, *, name = "Calibri", size = Pt(12), color = RGBColor(0,0,255), bold = True, italic = True):
        self.name = name
        self.size = size
        self.color = color
        self.bold = bold
        self.italic = italic


class PresentationFeature():

    table = [[None]*0]

    def __init__(self, strPPTXFilePath = ""):
        if strPPTXFilePath == "":
            self.prs = Presentation()
        else:
            self.prs = Presentation(strPPTXFilePath)

    # add text to a cell's run and new lines by the length of string_len
    @staticmethod
    def add_text_with_newlines(cell, list_ctry, *, string_len):
        str_ctry = ""
        for i in range(len(list_ctry)):
            if i > 0:
                str_ctry += ","
            str_ctry += list_ctry[i]

            if len(str_ctry) >= string_len:
                paragraph = cell.text_frame.paragraphs[-1]
                run = paragraph.add_run()
                run.text = str_ctry + "\n"
                str_ctry = ""

    @staticmethod
    def add_table(slide, row = 0, col = 0, left = 0, top = 0):
        shape = slide.shapes

        left = Inches(left)
        top = Inches(top)
        width = height = Inches(1)

        table = shape.add_table(row, col, left, top, width, height).table
        return table

    # format the column width and text size
    @staticmethod
    def resize_table(table, font_size):
        # setting font size
        for col in range(len(table.columns)):
            for row in range(len(table.rows)):
                for cell_pt in table.cell(row, col).text_frame.paragraphs:
                    cell_pt.font.size = font_size
        # format the column by finding the max length run in paragraphs
        list_col_max_width = [0 for x in range(len(table.columns))]
        for col in range(len(table.columns)):
            for row in range(len(table.rows)):
                for paragraphs in table.cell(row, col).text_frame.paragraphs:
                    for run in paragraphs.runs:
                        list_col_max_width[col] = max(list_col_max_width[col], len(run.text)*(font_size))
        # setting column width
        for col in range(len(table.columns)):
            table.columns[col].width = list_col_max_width[col] + Cm(0.25)

    # set cell text alignment by table
    @staticmethod
    def set_alignment(table, horizen_type, vertical_type):
        for row in range(len(table.rows)):
            for col in range(len(table.columns)):
                table.cell(row, col).vertical_anchor = vertical_type    # set vertical alignment
                for paragraph in table.cell(row, col).text_frame.paragraphs:
                    paragraph.alignment = horizen_type      # set horizen alignment

    # fill cell background
    @staticmethod
    def set_cell_fill(table, list_cell_coord, RGBcolor):
        for row, col in list_cell_coord:
            cell = table.cell(row, col)
            fill = cell.fill
            fill.solid()
            fill.fore_color.rgb = RGBcolor

    # fill table(all-cell) background
    @staticmethod
    def set_table_fill(table, RGBcolor):
        for row in range(len(table.rows)):
            for col in range(len(table.columns)):
                cell = table.cell(row, col)
                fill = cell.fill
                fill.solid()
                fill.fore_color.rgb = RGBcolor

    @staticmethod
    def SubElement(parent, tagname, **kwargs):
        element = OxmlElement(tagname)
        element.attrib.update(kwargs)
        parent.append(element)
        return element

    @classmethod
    def set_table_border(cls, table, border_color="000000", border_width='12700'):
        for row in range(len(table.rows)):
            for col in range(len(table.columns)):
                cell = table.cell(row, col)
                tc = cell._tc
                tcPr = tc.get_or_add_tcPr()

                lnR = cls.SubElement(
                    tcPr, 'a:lnR', w=border_width, cap='flat', cmpd='sng', algn='ctr')
                solidFill = cls.SubElement(lnR, 'a:solidFill')
                srgbClr = cls.SubElement(solidFill, 'a:srgbClr', val=border_color)
        #return table

    def save(self, strOutputPath):
        self.prs.save(strOutputPath)

    def add_slide(self, layout_idx):
        slide_layout = self.prs.slide_layouts[layout_idx]
        self.prs.slides.add_slide(slide_layout)

    def get_single_slide(self, slide_idx):
        return self.prs.slides[slide_idx]

    def get_slides(self):
        return self.prs.slides

    def add_picture(self, slide_idx, image_path):
        shapes = self.prs.slides[slide_idx].shapes

        left = top = Inches(1)
        width = Inches(16)
        height = Inches(10)

        pic = shapes.add_picture(image_path, left, top, width=width, height=height)


    def add_table_from_dataFrame(self, df, slide_idx, left = 0, top = 0):
        shapes = self.prs.slides[slide_idx].shapes

        left = Inches(left)
        top = Inches(top)
        width = height = Inches(0)

        rows = df.shape[0] + 1
        cols = df.shape[1]

        table = shapes.add_table(rows, cols, left, top, width, height).table

        for col in range(df.shape[1]):
            table.columns[col].height = Inches(2.0)
            for row in range(df.shape[0] + 1):
                if row == 0:
                    table.cell(row, col).text = str(df.columns[col])
                    continue
                table.cell(row, col).text = str(df.iloc[row - 1, col])
                # type(table.cell(row, col).text_frame.paragraphs) return 'tuple'

        #self.table[slide_idx].append(table)     # save table to a list of slides

        return table

    # read table as dataframe with row-multiIndex
    def read_table_as_dataFrame(self, table, *, col_header_count=1):

        # read the row_headers
        row_headers = []
        for i in range(col_header_count):
            column_name = []
            for col in range(len(table.columns)):
                column_name.append(table.cell(i, col).text_frame.text)
            row_headers.append(column_name)

        # read the remaining row-data
        row_data = []
        for row in range(col_header_count, len(table.rows)):
            col_data = []
            for col in range(len(table.columns)):
                col_data.append(table.cell(row, col).text_frame.text)
            row_data.append(col_data)

        # set row-multiIndex and create dataframe
        row_mutil_index = pd.MultiIndex.from_arrays(row_headers)
        df = pd.DataFrame(row_data, columns=row_mutil_index)

        return df



    # font cell text
    def font_cell(self, table, list_cells, Font):
        for row, col in list_cells:
            cell = table.cell(row, col)
            for paragraph in cell.text_frame.paragraphs:
                for run in paragraph.runs:
                    self.setFont(run, Font)

    # concatenate text to a cell
    def add_text_to_cell(self, strText, table, row, col, Font):
        cell = table.cell(row, col)
        paragraph = cell.text_frame.paragraphs[-1]
        run = paragraph.add_run()
        run.text = strText
        self.setFont(run, Font)

    # set text(run) font
    def setFont(self, run, Font):
        font = run.font
        font.name = Font.name
        font.size = Font.size
        font.color.rgb = Font.color
        font.bold = Font.bold
        font.italic = Font.italic


class TableDataFrame():

    def __init__(self):
        pass

    # read table as dataframe with row-multiIndex
    @staticmethod
    def read_table_as_dataFrame(self, table, *, col_header_count=1):

        # read the row_headers
        row_headers = []
        for i in range(col_header_count):
            column_name = []
            for col in range(len(table.columns)):
                column_name.append(table.cell(i, col).text_frame.text)
            row_headers.append(column_name)

        # read the remaining row-data
        row_data = []
        for row in range(col_header_count, len(table.rows)):
            col_data = []
            for col in range(len(table.columns)):
                col_data.append(table.cell(row, col).text_frame.text)
            row_data.append(col_data)

        # set row-multiIndex and create dataframe
        row_mutil_index = pd.MultiIndex.from_arrays(row_headers)
        df = pd.DataFrame(row_data, columns=row_mutil_index)

        return df

    @staticmethod
    def set_existing_column(df, list_val, lst_column, total_level):
        """
            The length of col_name and level must be the same.
        """
        try:
            print(df.shape)
            print(df.columns)

            print(df)
            list = np.random.rand(16, 1)
            print(list)

            idx = pd.IndexSlice[:, :, :]    # defalut setting: three layer of none slicing(None)
            for i in range(len(lst_column)):
                idx[i] = lst_column[i]

            df.loc[:,idx] = list
            print(df)

        except:
            pass
