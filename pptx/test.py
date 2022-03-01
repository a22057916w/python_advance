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
#from pptx.oxml.shapes.table import CT_Table

import xml.etree.ElementTree as ET
from lxml import etree

sys.path.append("./script")
from PPTX_FEATURE import Report, Font, TableDataFrame

g_strOutputPath = os.path.join("./result", os.path.basename(__file__)[:-3] + ".pptx")




def get_table_xml(strPPTXFilePath):
    clientRT = Report(strPPTXFilePath)
    slides = clientRT.get_slides()
    sld = slides[0]
    table = None

    for shape in sld.shapes:
        if shape.has_table:
            print("------------------------")
            table = shape.table
            #print(table._tbl)
            break
    with open("table_xml.xml", "w") as f:
        f.write(str(table._tbl.xml))

    cp_table = clientRT.add_table(table, 0)
    with open("copy_table_xml.xml", "w") as f:
        f.write(str(cp_table._tbl.xml))
    #tcPr = tc.get_or_add_tcPr()
    # for child in tc:
    #     print(child.tag)
    # e_txBody = tc.find("a:txBody", namespaces)
    # print(e_txBody.tag)
    root = ET.fromstring(table._tbl.xml)
    cp_table_root = ET.fromstring(cp_table._tbl.xml)
    copy_table_paragraph_xml(table, cp_table)
    clientRT.save("./result/test.pptx")


def copy_table_paragraph_xml(table, cp_table):
    namespaces = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    pPr = []
    for row in range(len(table.rows)):
        cell = table.cell(row, 0)
        tc = cell._tc
        txBody = tc.txBody
        pPr = txBody.find(".//a:pPr", namespaces)   # pPr: Represents the paragraph properties.
        print(pPr.tag)
    print("==========================")
    for element in [pPr[i] for i in range(len(pPr))]:
        print(element.tag, element.attrib)
    # print("==========================================================")
    # for row in range(len(table.rows)):
    #     cell = cp_table.cell(row, 0)
    #     tc = cell._tc
    #     txBody = tc.txBody
    #     pPr = txBody.find(".//a:pPr", namespaces)
    #     print(pPr)

def print_xml_tag(root):
    namespaces = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    for tr in root.findall("a:tr", namespaces):
        for tc in tr.findall("a:tc", namespaces):
            for txbody in tc.findall("a:txbody", namespaces):
                for p in txbody.findall("a:p", namespaces):
                    for pPr in p.findall("a:pPr", namespaces):
                        for defRPr in pPr.findall("a:defRPr", namespaces):
                            print(defRPr.attrib)

if __name__ == "__main__":
    print("sdfsdf")
    #create_pptx()
    #add_column("./example/Carnoustie_Mid Deep Dive_Regulatory schedule_20210225.pptx")
    get_table_xml("/data/Code/python/python_advance/pptx/result/report.pptx")
    # print(df)
    # print("*"*20)
    # print(df.shape)
    # print(df.shape[1])
