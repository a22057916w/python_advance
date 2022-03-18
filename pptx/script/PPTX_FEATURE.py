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

class PresentationFeature():

    table = [[None]*0]

    def __init__(self, strPPTXFilePath = ""):
        if strPPTXFilePath == "":
            self.prs = Presentation()
        else:
            self.prs = Presentation(strPPTXFilePath)

    @staticmethod
    def add_text(cell, str_text):
        paragraph = cell.text_frame.paragraphs[-1]
        run = paragraph.add_run()
        run.text = str_text

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

    @staticmethod
    def set_column_width(table, list_col_idx, *, width=Pt(1)):
        for col in list_col_idx:
            table.columns[col].width = width


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

    # new xml element to set style
    @staticmethod
    def SubElement(parent, tagname, **kwargs):
        element = OxmlElement(tagname)
        element.attrib.update(kwargs)
        parent.append(element)
        return element


    # set border style by modifying xml
    @classmethod
    def set_table_border(cls, table, border_color="444444", border_width='12700'):
        for row in range(len(table.rows)):
            for col in range(len(table.columns)):
                cell = table.cell(row, col)
                tc = cell._tc                   # <class 'pptx.oxml.table.CT_TableCell'> as a xml element
                tcPr = tc.get_or_add_tcPr()     # <class 'pptx.oxml.table.CT_TableCellProperties'> as a xml element
                for lines in ['a:lnL','a:lnR','a:lnT','a:lnB']:
                    ln = cls.SubElement(tcPr, lines, w=border_width, cap='flat', cmpd='sng', algn='ctr')
                    solidFill = cls.SubElement(ln, 'a:solidFill')
                    srgbClr = cls.SubElement(solidFill, 'a:srgbClr', val=border_color)
                    prstDash = cls.SubElement(ln, 'a:prstDash', val='solid')
                    # round_ = cls.SubElement(ln, 'a:round')
                    # headEnd = cls.SubElement(ln, 'a:headEnd', type='none', w='med', len='med')
                    # tailEnd = cls.SubElement(ln, 'a:tailEnd', type='none', w='med', len='med')
