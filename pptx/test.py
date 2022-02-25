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

    cp_tbl = clientRT.add_table(table, 0)
    with open("copy_table_xml.xml", "w") as f:
        f.write(str(cp_tbl._tbl.xml))

    root = ET.fromstring(table._tbl.xml)
    #print(root.tag)
    test_xml(root)

    clientRT.save("./result/test.pptx")

def test_xml(root):
    print("=================================")
    for cld in root:
        print(cld.tag)
    pass


if __name__ == "__main__":
    print("sdfsdf")
    #create_pptx()
    #add_column("./example/Carnoustie_Mid Deep Dive_Regulatory schedule_20210225.pptx")
    get_table_xml("/data/Code/python/python_advance/pptx/result/report.pptx")
    # print(df)
    # print("*"*20)
    # print(df.shape)
    # print(df.shape[1])
