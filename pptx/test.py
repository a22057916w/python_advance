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

import zipfile


def get_table_xml(strPPTXFilePath):
    clientRT = Report(strPPTXFilePath)
    slides = clientRT.get_slides()
    sld = slides[0]
    table = None

    for shape in sld.shapes:
        if shape.has_table:
            table = shape.table
            break

    with open("table_xml.xml", "w") as f:
        f.write(str(table._tbl.xml))

    cp_table = clientRT.add_table(table, 0)
    #clientRT.resize_table(cp_table, Pt(12))
    with open("copy_table_xml.xml", "w") as f:
        f.write(str(cp_table._tbl.xml))

    #
    # root = ET.fromstring(table._tbl.xml)
    # print(root)
    # print(ET.fromstring(table._tbl.xml))
    # cp_root = ET.fromstring(cp_table._tbl.xml)
    #traverse_xml(root)
    #traverse_xml(cp_root)
    #copy_tc_xml(root, cp_root)
    # with open("copied_table_xml.xml", "w") as f:
    #     f.write(str(cp_table._tbl.xml))
    # print("++++++++++++++++++++++++++++")
    #traverse_xml(cp_root)
    #ET.dump(cp_root)
    for row in range(len(table.rows)):
        for col in range(len(table.columns)):
            tc_src = table.cell(row, col)._tc
            tc_cp = cp_table.cell(row, col)._tc
            # traverse_xml(tc_cp)
            # copy_tc_xml(tc_src, tc_cp)
            # print("=======================")
            traverse_xml(tc_src)
            # print("check")
            # traverse_xml(tc_cp)
            return

    clientRT.save("./result/test.pptx")

def traverse_xml(root):
    namespaces = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
    if root == None:
        print("Element is None")
        return

    for element in root:
        print(element.tag, element.attrib)
        traverse_xml(element)

def copy_tc_xml(tc_src, tc_cp):
    namespaces = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}

    if tc_src == None or tc_cp == None:
        return

    #print(tc_src[0].tag)
    for element in tc_src:
        #print(element.tag, element.attrib)
        #print("sdfsdf")
        cp_element = tc_cp.find(element.tag)
        if cp_element != None:
            #print(dict(element.attrib))
            #print(cp_element)
            set_element_attrib(cp_element, dict(element.attrib))
            copy_tc_xml(element, cp_element)
        else:
            # print(tc_cp.tag)
            # print(element.tag)
            # print(dict(element.attrib))
            subelement = ET.SubElement(tc_cp, element.tag, dict(element.attrib))
            #print(element.tag, subelement.tag)
            copy_tc_xml(element, subelement)
            #print(tc_cp.tag, element.tag)


def set_element_attrib(target_element, dict_attrib):
    #print(dict_attrib)
    #print(target_element.tag)
    #print(target_element)
    for key, item in dict_attrib.items():
        #print(key, item)
        target_element.set(key, item)
    #print(target_element.tag, target_element.attrib)

def read_pptx_xml():
    archive = zipfile.ZipFile('./result/xml/test.pptx', 'r')
    xml_file = archive.open('[Content_Types].xml')
    text = xml_file.read()

    root = ET.fromstring(text)
    value_to_find = r'application/vnd.openxmlformats-package.relationships+xml'
    for child in root:
        if child.attrib['ContentType'] == value_to_find:
            print(child.attrib)

# def copy_table_paragraph_xml(table, cp_table):
#     namespaces = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
#     paragraph = []
#     pPr = []
#     for row in range(len(table.rows)):
#         cell = table.cell(row, 0)
#         tc = cell._tc
#         txBody = tc.txBody
#         paragraph = txBody.findall(".//a:p", namespaces)
#         # pPr = txBody.find(".//a:pPr", namespaces)   # pPr: Represents the paragraph properties.
#         # print(pPr.tag)
#     print(paragraph[0].tag)
#     print("==========================")

    # if pPr != None:
    #     for element in [pPr[i] for i in range(len(pPr))]:
    #         print(element.tag, element.attrib)

    # print("==========================================================")
    # for row in range(len(cp_table.rows)):
    #     cell = cp_table.cell(row, 0)
    #     tc = cell._tc
    #     cp_txBody = tc.txBody
    #     for element in [pPr[i] for i in range(len(pPr))]:
    #         str_tag = element.tag
    #         dict_attrib = dict(element.attrib)
    #         # print(tag, attrib)
    #         # print(type(tag), type(dict(attrib)))
    #         parent = ET.Element(cp_txBody)
    #         # print(cp_txBody)
    #         # print(parent)
    #         pPr_child = ET.SubElement(parent, str_tag, dict_attrib)

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
    #create_pptx()
    #add_column("./example/Carnoustie_Mid Deep Dive_Regulatory schedule_20210225.pptx")
    #get_table_xml("/data/Code/python/python_advance/pptx/result/table.pptx")
    read_pptx_xml()
    # print(df)
    # print("*"*20)
    # print(df.shape)
    # print(df.shape[1])
